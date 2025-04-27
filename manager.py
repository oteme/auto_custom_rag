# manager.py

from registry import ModuleRegistry

class PipelineManager:
    def __init__(self, config: dict):
        self.config = config
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
        self.model = None

    def initialize_pipeline(self):
        self.check_pipeline_compatibility()
        # Data Pipeline
        data_cfg = self.config["data_pipeline"]

        for loader_name in data_cfg["loaders"]:
            LoaderClass = ModuleRegistry.get_class(loader_name)
            loader_params = data_cfg.get("loader_params", {}).get(loader_name, {})
            loader_instance = LoaderClass(**loader_params)
            self.loaders.append(loader_instance)

        ParserClass = ModuleRegistry.get_class(data_cfg["parser"])
        parser_params = data_cfg.get("parser_params", {}).get(data_cfg["parser"], {})
        self.parser = ParserClass(**parser_params)

        NormalizerClass = ModuleRegistry.get_class(data_cfg["normalizer"])
        normalizer_params = data_cfg.get("normalizer_params", {}).get(data_cfg["normalizer"], {})
        self.normalizer = NormalizerClass(**normalizer_params)

        ChunkerClass = ModuleRegistry.get_class(data_cfg["chunker"])
        chunker_params = data_cfg.get("chunker_params", {}).get(data_cfg["chunker"], {})
        self.chunker = ChunkerClass(**chunker_params)

        EmbedderClass = ModuleRegistry.get_class(data_cfg["embedder"])
        embedder_params = data_cfg.get("embedder_params", {}).get(data_cfg["embedder"], {})
        self.embedder = EmbedderClass(**embedder_params)

        # Retrieval Pipeline
        retrieval_cfg = self.config["retrieval_pipeline"]

        RetrieverClass = ModuleRegistry.get_class(retrieval_cfg["retriever"])
        retriever_params = retrieval_cfg.get("retriever_params", {})
        self.retriever = RetrieverClass(**retriever_params)

        for filter_name in retrieval_cfg["filters"]:
            FilterClass = ModuleRegistry.get_class(filter_name)
            filter_params = retrieval_cfg.get("filter_params", {}).get(filter_name, {})
            filter_instance = FilterClass(**filter_params)
            self.filters.append(filter_instance)

        RerankerClass = ModuleRegistry.get_class(retrieval_cfg["reranker"])
        reranker_params = retrieval_cfg.get("reranker_params", {}).get(retrieval_cfg["reranker"], {})
        self.reranker = RerankerClass(**reranker_params)

        # Generation Pipeline
        generation_cfg = self.config["generation_pipeline"]

        PromptTemplateClass = ModuleRegistry.get_class(generation_cfg["prompt_template"])
        prompt_params = generation_cfg.get("prompt_template_params", {}).get(generation_cfg["prompt_template"], {})
        self.prompt_template = PromptTemplateClass(**prompt_params)

        for postprocessor_name in generation_cfg["postprocessors"]:
            PostProcessorClass = ModuleRegistry.get_class(postprocessor_name)
            postprocessor_params = generation_cfg.get("postprocessor_params", {}).get(postprocessor_name, {})
            postprocessor_instance = PostProcessorClass(**postprocessor_params)
            self.postprocessors.append(postprocessor_instance)

        # Model (optional)
        model_cfg = self.config.get("model")
        if model_cfg:
            ModelClass = ModuleRegistry.get_class(model_cfg["name"])
            model_params = model_cfg.get("params", {})
            self.model = ModelClass(**model_params)

    def ingest(self):
        all_chunks = []
        for loader in self.loaders:
            for raw_doc in loader.load():
                parsed_doc = self.parser.parse(raw_doc)
                normalized_doc = self.normalizer.normalize(parsed_doc)
                chunks = self.chunker.chunk(normalized_doc)
                all_chunks.extend(chunks)

        if hasattr(self.retriever, "ingest"):
            self.retriever.ingest(all_chunks, self.embedder)

    def query(self, user_query: str):
        retrieved_chunks = self.retriever.retrieve(user_query)

        filtered_chunks = retrieved_chunks
        for filter_module in self.filters:
            filtered_chunks = filter_module.filter(filtered_chunks, user_query)

        reranked_chunks = self.reranker.rerank(filtered_chunks, user_query)
        prompt = self.prompt_template.format_prompt(user_query, reranked_chunks)

        llm_response = self.model.generate(prompt) if self.model else f"Dummy response for prompt: {prompt[:30]}..."

        final_response = llm_response
        for postprocessor in self.postprocessors:
            final_response = postprocessor.postprocess(final_response)

        print("Final Response:")
        print(final_response)

    def check_pipeline_compatibility(self):
        print("[Manager] Checking pipeline compatibility...")

        data_cfg = self.config["data_pipeline"]
        module_sequence = []

        for loader_name in data_cfg["loaders"]:
            module_sequence.append(loader_name)
        module_sequence.append(data_cfg["parser"])
        module_sequence.append(data_cfg["normalizer"])
        module_sequence.append(data_cfg["chunker"])
        module_sequence.append(data_cfg["embedder"])

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
