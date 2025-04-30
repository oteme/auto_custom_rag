# manager.py  – Flow 駆動型（pipelines/orchestrator 対応版）
# --------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Dict, List, Optional

from registry import ModuleRegistry


class PipelineManager:
    """
    役割
    -------
    1. config["pipelines"] 内で参照されるモジュールを 1 度だけ new してキャッシュ
    2. orchestrator.flow に従い各パイプラインを順実行し最終結果を返す
    3. 全ステップの manifest.yaml を読み、隣接モジュール I/O の型整合性をチェック
    """

    # 遅延バインド（Manager 生成時にはインスタンス化しない）タイプ
    LATE_BIND_TYPES = {"dialogue_ctrl", "ui_adapter"}

    # ----------------------------------------------------------------
    # 初期化
    # ----------------------------------------------------------------
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self._module_cache: Dict[str, Any] = {}
        self.retrievers: Dict[str, Any] = {}            # ingest 済みを保持

        self._build_modules()
        self.check_pipeline_compatibility()

    # ----------------------------------------------------------------
    # モジュール生成（1 回のみ）
    # ----------------------------------------------------------------
    def _build_modules(self) -> None:
        """
        pipelines.*.steps と orchestrator.*（session_manager など）を走査し
        必要なクラスを import・new・キャッシュする。
        """
        def _instantiate(step: dict) -> None:
            if step["type"] in self.LATE_BIND_TYPES:
                return

            name   = step["name"]
            params = dict(step.get("params", {}))

            # retriever だけシステム都合のフラグを抜く
            if step["type"] == "retriever":
                params.pop("embedding_required", None)

            if name not in self._module_cache:
                cls = ModuleRegistry.get_class(name)
                self._module_cache[name] = cls(**params)

        # --- pipelines.* 内の全ステップ
        for pipe in self.config["pipelines"].values():
            for st in pipe["steps"]:
                _instantiate(st)

        # --- orchestrator 直下（session_manager / dialogue / ui）
        orch = self.config.get("orchestrator", {})
        for key in ("session_manager", "dialogue_ctrl", "ui_adapter"):
            if key in orch:
                _instantiate({**orch[key], "type": key})

    # ----------------------------------------------------------------
    # public API
    # ----------------------------------------------------------------
    def run_flow(self, flow: List[str], query: str = "") -> Any:
        """
        orchestrator.flow で指定された pipeline 名を順に走査。
        パイプラインごとに _run_<name>() を呼び、最後の戻りを返す。
        """
        data = None
        for pipeline_key in flow:
            data = getattr(self, f"_run_{pipeline_key}")(data, query)
        return data

    # ----------------------------------------------------------------
    # 個別パイプライン実装
    # ----------------------------------------------------------------
    # --- data --------------------------------------------------------
    def _run_data(self, *_):
        pipe = self.config["pipelines"]["data"]
        all_chunks: list[Any] = []
        embedder = None

        # Loader / Parser / Normalizer / Chunker / Embedder を順に処理
        for step in pipe["steps"]:
            typ, name = step["type"], step["name"]
            mod = self._module_cache[name]

            if typ == "loader":
                all_chunks.extend(mod.load())

            elif typ == "parser":
                all_chunks = [mod.parse(d) for d in all_chunks]

            elif typ == "normalizer":
                all_chunks = [mod.normalize(d) for d in all_chunks]

            elif typ == "chunker":
                tmp = []
                for doc in all_chunks:
                    tmp.extend(mod.chunk(doc))
                all_chunks = tmp

            elif typ == "embedder":
                embedder = mod                       # ingest 用に保持

        
        return all_chunks

    # --- retrieval ---------------------------------------------------
    def _run_retrieval(self, _, query: str):
        # --- まだベクトル DB が空なら ingest を実施 -----------------
        if not self.retrievers:          # 初回かどうかの簡易判定
            chunks = self._run_data(None, None)
            embedder_name = next(s["name"] for s in self.config["pipelines"]["retrieval"]["steps"]
                                 if s["type"] == "embedder")
            embedder = self._module_cache[embedder_name]
            for st in self.config["pipelines"]["retrieval"]["steps"]:
                if st["type"] == "retriever":
                    r = self._module_cache[st["name"]]
                    r.ingest(chunks, embedder)
                    self.retrievers[st["name"]] = r

        data, buffer = query, []

        r_steps = self.config["pipelines"]["retrieval"]["steps"]

        # 事前に “先頭の embedder” を取得（埋め込みが必要な retriever 用）
        first_embedder_name = next(
            (s["name"] for s in r_steps if s["type"] == "embedder"), None
        )
        first_embedder = self._module_cache[first_embedder_name] if first_embedder_name else None

        for st in r_steps:
            typ, name, params = st["type"], st["name"], st.get("params", {})
            mod = self._module_cache[name]

            if typ == "embedder":
                data = mod.embed(data) if isinstance(data, str) else data

            elif typ == "retriever":
                # 未 ingest の場合は lazy-ingest
                if name not in self.retrievers:
                    chunks = self._run_data(None, None)
                    mod.ingest(chunks, first_embedder)
                    self.retrievers[name] = mod

                retriever = self.retrievers[name]
                if params.get("embedding_required", False) and isinstance(data, str):
                    data_vec = first_embedder.embed(data)
                else:
                    data_vec = data
                buffer.extend(retriever.retrieve(data_vec))

            elif typ == "retrieval_merge":
                buffer = mod.merge(buffer)

            elif typ == "filter":
                buffer = mod.filter(buffer, query)

            elif typ == "reranker":
                buffer = mod.rerank(buffer, query)

        return buffer

    # --- generation --------------------------------------------------
    def _run_generation(self, chunks, query: str):
        g_steps = self.config["pipelines"]["generation"]["steps"]

        prompt_str: str = query
        postprocessors: list[Any] = []

        for st in g_steps:
            typ, name, params = st["type"], st["name"], st.get("params", {})
            mod = self._module_cache[name]

            if typ == "prompt_template":
                prompt_str = mod.format_prompt(prompt_str, chunks)

            elif typ == "model":
                prompt_str = mod.generate(prompt_str)

            elif typ == "postprocessor":
                postprocessors.append(mod)

        for pp in postprocessors:
            prompt_str = pp.postprocess(prompt_str)

        return prompt_str

    # ----------------------------------------------------------------
    # パイプライン互換性チェック
    # ----------------------------------------------------------------
    def check_pipeline_compatibility(self) -> None:
        """
        pipelines.* の steps を走査し、
        manifest.yaml の inputs / outputs 型が隣接で 1 つでも重なるか確認。
        一致ゼロなら WARNING を表示（実行は続行）。
        """
        print("[Manager] Checking pipeline compatibility...")

        def _types(meta: dict, key: str) -> list[str]:
            return [item["type"] for item in meta.get(key, [])]

        def _compatible(prev_out: list[str], curr_in: list[str]) -> bool:
            return bool(set(prev_out) & set(curr_in))

        def _validate(steps: list[dict]) -> None:
            prev_out, prev_name = None, None
            for st in steps:
                meta = ModuleRegistry.get_metadata(st["name"])
                in_t, out_t = _types(meta, "inputs"), _types(meta, "outputs")

                if prev_out is not None and not _compatible(prev_out, in_t):
                    print(f"[WARNING] 型不一致: {prev_name} -> {st['name']}")
                    print(f"  出力型: {prev_out}")
                    print(f"  入力型: {in_t}")

                prev_out, prev_name = out_t, st["name"]

        for pipe in self.config["pipelines"].values():
            _validate(pipe["steps"])
