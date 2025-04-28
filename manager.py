# manager.py
# ------------------------------------------------------------------
#  auto-custom-rag – PipelineManager 〈完成版〉
# ------------------------------------------------------------------

from registry import ModuleRegistry


class PipelineManager:
    def __init__(self, config: dict):
        self.config = config

        # --- 各モジュール初期化用 ---
        self.loaders = []
        self.parser = None
        self.normalizer = None
        self.chunker = None
        self.embedder = None

        self.retriever = None
        self.filters = []
        self.reranker = None

        self.prompt_template = None
        self.postprocessors = []

        self.session_manager = None
        self.model = None
        self.mode_runner = None

    # --------------------------------------------------------------
    # パイプライン初期化（モジュールロード）
    # --------------------------------------------------------------
    def initialize_pipeline(self):
        self.check_pipeline_compatibility()
        # --- Data Pipeline ---
        dp = self.config.get("data_pipeline", {})

        for loader_conf in dp.get("loaders", []):
            Loader = ModuleRegistry.get_class(loader_conf["name"])
            self.loaders.append(Loader(**loader_conf.get("params", {})))

        if dp.get("parser"):
            Parser = ModuleRegistry.get_class(dp["parser"]["name"])
            self.parser = Parser(**dp["parser"].get("params", {}))

        if dp.get("normalizer"):
            Normalizer = ModuleRegistry.get_class(dp["normalizer"]["name"])
            self.normalizer = Normalizer(**dp["normalizer"].get("params", {}))

        if dp.get("chunker"):
            Chunker = ModuleRegistry.get_class(dp["chunker"]["name"])
            self.chunker = Chunker(**dp["chunker"].get("params", {}))

        if dp.get("embedder"):
            Embedder = ModuleRegistry.get_class(dp["embedder"]["name"])
            self.embedder = Embedder(**dp["embedder"].get("params", {}))

        # --- Retrieval Pipeline ---
        retrieval_steps = self.config.get("retrieval_pipeline", {}).get("steps", [])

        for step in retrieval_steps:
            step_type = step["type"]
            step_name = step["name"]
            params = step.get("params", {})

            if step_type == "retriever":
                RetrieverClass = ModuleRegistry.get_class(step_name)
                self.retriever = RetrieverClass(**params)

            elif step_type == "filter":
                FilterClass = ModuleRegistry.get_class(step_name)
                filter_instance = FilterClass(**params)
                self.filters.append(filter_instance)

            elif step_type == "reranker":
                RerankerClass = ModuleRegistry.get_class(step_name)
                self.reranker = RerankerClass(**params)

            else:
                raise ValueError(f"Unknown retrieval step type: {step_type}")

        # --- Generation Pipeline ---
        gp = self.config.get("generation_pipeline", {})

        if gp.get("prompt_template"):
            PT = ModuleRegistry.get_class(gp["prompt_template"]["name"])
            self.prompt_template = PT(**gp["prompt_template"].get("params", {}))

        for postprocessor_conf in gp.get("postprocessors", []):
            PP = ModuleRegistry.get_class(postprocessor_conf["name"])
            self.postprocessors.append(PP(**postprocessor_conf.get("params", {})))

        # --- Runtime Pipeline ---
        rt = self.config.get("runtime_pipeline", {})

        if rt.get("session_manager"):
            SM = ModuleRegistry.get_class(rt["session_manager"]["name"])
            self.session_manager = SM(**rt["session_manager"].get("params", {}))

        if rt.get("model"):
            Model = ModuleRegistry.get_class(rt["model"]["name"])
            self.model = Model(**rt["model"].get("params", {}))

        if rt.get("mode"):
            Mode = ModuleRegistry.get_class(rt["mode"]["name"])
            self.mode_runner = Mode(manager=self, **rt["mode"].get("params", {}))

    # --------------------------------------------------------------
    # フローに従ってパイプラインを順次実行
    # --------------------------------------------------------------
    def run(self):
        for step in self.config.get("flow", []):
            if step == "data_pipeline":
                self._run_data_pipeline()
            elif step == "retrieval_pipeline":
                pass  # retrievalは通常runtimeで内部的に使う
            elif step == "generation_pipeline":
                pass  # generationも通常runtimeで内部的に使う
            elif step == "runtime_pipeline":
                if not self.mode_runner:
                    raise ValueError("ModeRunner not initialized")
                self.mode_runner.run()
            else:
                raise ValueError(f"[Manager] Unknown flow step: {step}")

    # --------------------------------------------------------------
    # データ取り込みパイプラインのみ個別実行
    # --------------------------------------------------------------
    def _run_data_pipeline(self):
        all_chunks = []
        for loader in self.loaders:
            raw_docs = loader.load()
            for raw_doc in raw_docs:
                parsed = self.parser.parse(raw_doc)
                normalized = self.normalizer.normalize(parsed)
                chunks = self.chunker.chunk(normalized)
                all_chunks.extend(chunks)

        if hasattr(self.retriever, "ingest"):
            self.retriever.ingest(all_chunks, self.embedder)

    # --------------------------------------------------------------
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

    def retrieve_chunks(self, query: str):
        """retrieval_pipeline.stepsに基づき柔軟にchunk retrievalを行う"""
        chunks = None
        steps = self.config["retrieval_pipeline"]["steps"]

        for step in steps:
            module_type = step["type"]

            if module_type == "retriever":
                chunks = self.retriever.retrieve(query)

            elif module_type == "filter":
                for filter_module in self.filters:
                    chunks = filter_module.filter(chunks, query)

            elif module_type == "reranker":
                chunks = self.reranker.rerank(chunks, query)

            else:
                raise ValueError(f"Unknown retrieval step type: {module_type}")

        return chunks

