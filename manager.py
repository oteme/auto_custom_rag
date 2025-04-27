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

    def initialize_pipeline(self):
        # Data Pipeline
        loader_names = self.config["data_pipeline"]["loaders"]
        parser_name = self.config["data_pipeline"]["parser"]
        normalizer_name = self.config["data_pipeline"]["normalizer"]
        chunker_name = self.config["data_pipeline"]["chunker"]
        embedder_name = self.config["data_pipeline"]["embedder"]

        for loader_name in loader_names:
            LoaderClass = ModuleRegistry.get_class(loader_name)
            loader_instance = LoaderClass(path="sample_data/")
            self.loaders.append(loader_instance)

        ParserClass = ModuleRegistry.get_class(parser_name)
        NormalizerClass = ModuleRegistry.get_class(normalizer_name)
        ChunkerClass = ModuleRegistry.get_class(chunker_name)
        EmbedderClass = ModuleRegistry.get_class(embedder_name)

        self.parser = ParserClass()
        self.normalizer = NormalizerClass()
        self.chunker = ChunkerClass()
        self.embedder = EmbedderClass()

        # Retrieval Pipeline
        retriever_name = self.config["retrieval_pipeline"]["retriever"]
        filter_names = self.config["retrieval_pipeline"]["filters"]
        reranker_name = self.config["retrieval_pipeline"]["reranker"]

        RetrieverClass = ModuleRegistry.get_class(retriever_name)
        self.retriever = RetrieverClass()

        for filter_name in filter_names:
            FilterClass = ModuleRegistry.get_class(filter_name)
            filter_instance = FilterClass()
            self.filters.append(filter_instance)

        RerankerClass = ModuleRegistry.get_class(reranker_name)
        self.reranker = RerankerClass()

        # Generation Pipeline
        prompt_template_name = self.config["generation_pipeline"]["prompt_template"]
        postprocessor_names = self.config["generation_pipeline"]["postprocessors"]

        PromptTemplateClass = ModuleRegistry.get_class(prompt_template_name)
        self.prompt_template = PromptTemplateClass()

        for postprocessor_name in postprocessor_names:
            PostProcessorClass = ModuleRegistry.get_class(postprocessor_name)
            postprocessor_instance = PostProcessorClass()
            self.postprocessors.append(postprocessor_instance)

    def ingest(self):
        for loader in self.loaders:
            raw_docs = loader.load()
            for raw_doc in raw_docs:
                parsed_doc = self.parser.parse(raw_doc)
                normalized_doc = self.normalizer.normalize(parsed_doc)
                chunks = self.chunker.chunk(normalized_doc)
                for chunk in chunks:
                    vector = self.embedder.embed(chunk)
                    # 今はダミーなのでベクトル保存しない

    def query(self, user_query: str):
        retrieved_chunks = self.retriever.retrieve(user_query)

        filtered_chunks = retrieved_chunks
        for filter_module in self.filters:
            filtered_chunks = filter_module.filter(filtered_chunks, user_query)

        reranked_chunks = self.reranker.rerank(filtered_chunks, user_query)
        prompt = self.prompt_template.format_prompt(user_query, reranked_chunks)

        # ダミーのLLMレスポンス（本来はLLMにpromptを投げる）
        dummy_llm_response = f"Generated answer based on prompt: {prompt[:30]}..."

        final_response = dummy_llm_response
        for postprocessor in self.postprocessors:
            final_response = postprocessor.postprocess(final_response)

        print("Final Response:")
        print(final_response)
