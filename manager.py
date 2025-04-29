# manager.py  ── Flow 駆動型にリファクタ＋compatibility チェック強化
# --------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Dict, List, Optional

from registry import ModuleRegistry

class PipelineManager:
    """
    役割:
        1. config を読み込みモジュールを 1 回だけ new する
        2. flow 配列どおりに各パイプラインを順実行する
        3. manifest.yaml に従い I/O 型の整合性を実行前に検証する
    """
    # ──────────────────────────────
    # 初期化
    # ──────────────────────────────
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self._module_cache: Dict[str, Any] = {}
        self.retrievers: Dict[str, Any] = {}         # ingest 再利用用
        self._build_modules()                        # new はここだけ
        self.check_pipeline_compatibility()          # ★ 互換性チェック

    # ──────────────────────────────
    # モジュール生成（1 回のみ）
    # ──────────────────────────────
    def _build_modules(self) -> None:
        """config 内で参照されるすべてのモジュールを new して cache"""
        for pipe_key in (
            "data_pipeline", "retrieval_pipeline",
            "generation_pipeline", "runtime_pipeline"   # ← 既存
        ):
            block = self.config.get(pipe_key, {})
            # ─────────────────────────
            # ★ runtime_pipeline は steps を持たない
            #    → key ごとに明示的に new する
            # ─────────────────────────
            # manager.py  _build_modules() 内 runtime_pipeline 部分だけ修正
            if pipe_key == "runtime_pipeline" and block:
                for key in ("session_manager", "model", "dialogue_ctrl"):
                    item = block.get(key)
                    if not item:
                        continue
                    name   = item["name"]
                    params = item.get("params", {})

                    # ────────────────
                    # dialogue_ctrl は new しない
                    # ────────────────
                    if key == "dialogue_ctrl":
                        # キャッシュにクラスだけ入れておく（なくても可）
                        if name not in self._module_cache:
                            self._module_cache[name] = ModuleRegistry.get_class(name)
                        continue

                    # session_manager / model はここでインスタンス生成
                    if name not in self._module_cache:
                        cls = ModuleRegistry.get_class(name)
                        self._module_cache[name] = cls(**params)
                continue  # runtime_pipeline の処理はここで終わり
  # runtime_pipeline の処理はここで完了

            # ここから下は従来どおり  (data / retrieval / generation)
            steps = block["steps"] if pipe_key == "retrieval_pipeline" else [block] if block else []
            for step in steps:
                name = step.get("name") or step.get("loader")
                if not name or name in self._module_cache:
                    continue
                params = dict(step.get("params", {}))
                if pipe_key == "retrieval_pipeline" and step["type"] == "retriever":
                    params.pop("embedding_required", None)
                cls = ModuleRegistry.get_class(name)
                self._module_cache[name] = cls(**params)
    # ──────────────────────────────
    # public API
    # ──────────────────────────────
    def run_flow(self, flow: List[str], query: str = "") -> Any:
        """
        flow で指定されたパイプラインを順番に実行し、
        最終結果（LLM 出力 or chunks など）を返す
        """
        data = None
        for pipeline_key in flow:
            data = getattr(self, f"_run_{pipeline_key}")(data, query)
        return data

    # ──────────────────────────────
    # 個別パイプライン実装
    # ──────────────────────────────
    def _run_data_pipeline(self, *_):
        all_chunks = []
        dp = self.config["data_pipeline"]
        loader_confs = dp.get("loaders", [])
        for l_conf in loader_confs:
            loader = self._module_cache[l_conf["name"]]
            for raw in loader.load():
                parsed      = self._module_cache[dp["parser"]["name"]].parse(raw)
                normalized  = self._module_cache[dp["normalizer"]["name"]].normalize(parsed)
                chunks      = self._module_cache[dp["chunker"]["name"]].chunk(normalized)
                all_chunks.extend(chunks)

        # ingest（new 済 retriever を reuse）
        for step in self.config["retrieval_pipeline"]["steps"]:
            if step["type"] == "retriever":
                name = step["name"]
                if name not in self.retrievers:
                    self.retrievers[name] = self._module_cache[name]
                retriever = self.retrievers[name]
                if hasattr(retriever, "ingest"):
                    retriever.ingest(all_chunks, self._module_cache[ self.config["data_pipeline"]["embedder"]["name"] ])
        return all_chunks                       # for debug / optional

    def _run_retrieval_pipeline(self, _, query: str):
        data = query
        buffer = []
        for step in self.config["retrieval_pipeline"]["steps"]:
            typ, name, params = step["type"], step["name"], step.get("params", {})
            module = self._module_cache[name]

            if typ == "embedder":
                data = module.embed(data) if isinstance(data, str) else data

            elif typ == "retriever":
                retriever = self.retrievers[name]
                emb_req = params.get("embedding_required", False)
                q_vec = self._module_cache[ step["name_embedder"] ].embed(data) if emb_req and isinstance(data, str) else data
                buffer.extend(retriever.retrieve(q_vec))

            elif typ == "retrieval_merge":
                buffer = module.merge(buffer)

            elif typ == "filter":
                buffer = module.filter(buffer, query)

            elif typ == "reranker":
                buffer = module.rerank(buffer, query)

        return buffer                            # → generation_pipeline

    def _run_generation_pipeline(self, chunks, query: str):
        gp = self.config["generation_pipeline"]
        prompt = self._module_cache[ gp["prompt_template"]["name"] ].format_prompt(query, chunks)
        response = self._module_cache[ self.config["runtime_pipeline"]["model"]["name"] ].generate(prompt)
        for pp_conf in gp.get("postprocessors", []):
            response = self._module_cache[ pp_conf["name"] ].postprocess(response)
        return response

    def _run_runtime_pipeline(self, response, *_):
        # 今は postprocess 済みのレスポンスをそのまま返すだけ
        return response

    #--------------------------------------------------------------
    # パイプライン互換性チェック
    # --------------------------------------------------------------
    def check_pipeline_compatibility(self):
        print("[Manager] Checking pipeline compatibility...")

        data_cfg = self.config.get("data_pipeline")
        module_sequence = []

        for loader_conf in data_cfg.get("loaders", []):
            module_sequence.append(loader_conf["name"])
        module_sequence.append(data_cfg["parser"]["name"])
        module_sequence.append(data_cfg["normalizer"]["name"])
        module_sequence.append(data_cfg["chunker"]["name"])
        module_sequence.append(data_cfg["embedder"]["name"])

        previous_outputs = None
        previous_module = None

        for module_name in module_sequence:
            metadata = ModuleRegistry.get_metadata(module_name)
            inputs = metadata.get("inputs", [])
            outputs = metadata.get("outputs", [])

            if previous_outputs is not None:
                prev_types = [item["type"] for item in previous_outputs]
                curr_types = [item["type"] for item in inputs]

                if not any(pt in curr_types for pt in prev_types):
                    print(f"[WARNING] 型不一致: {previous_module} -> {module_name}")
                    print(f"  出力型: {prev_types}")
                    print(f"  入力型: {curr_types}")

            previous_outputs = outputs
            previous_module = module_name

# --------------------------------------------------------------------
# 例: 使い方
# from config_for_test import config
# manager = PipelineManager(config)
# result = manager.run_flow(config["flow"], query="Tell me about tropical rainforests")
# print(result)
