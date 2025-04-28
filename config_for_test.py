# config_for_test.py

config = {
    "data_pipeline": {
        "loaders": [
            {"name": "pdf_loader", "params": {"path": "data/pdfs/"}}
        ],
        "parser": {"name": "simple_parser", "params": {}},
        "normalizer": {"name": "basic_normalizer", "params": {}},
        "chunker": {"name": "simple_chunker", "params": {}},
        "embedder": {"name": "hf_embedder", "params": {"model_name": "all-MiniLM-L6-v2"}},
    },
    "retrieval_pipeline": {
        "steps": [
            {"type": "embedder", "name": "hf_embedder", "params": {"model_name": "all-MiniLM-L6-v2"}},

            {"type": "retriever", "name": "faiss_retriever", "params": {"embedding_required": True, "embedding_dim": 384, "top_k": 5}},
            {"type": "retrieval_merge", "name": "unique_merge", "params": {}},

            {"type": "retriever", "name": "bm25_retriever", "params": {"embedding_required": False, "top_k": 5}},  
            {"type": "retrieval_merge", "name": "score_max_merge", "params": {}},

            {"type": "filter", "name": "simple_score_filter", "params": {"threshold": 0.5}},
            {"type": "filter", "name": "metadata_filter", "params": {"key": "source", "allowed_values": ["important_doc1.pdf", "important_doc2.pdf"]}},

            {"type": "reranker", "name": "simple_reranker", "params": {}}
        ]
    },
    "generation_pipeline": {
        "prompt_template": {"name": "simple_prompt_template", "params": {}},
        "postprocessors": [
            {"name": "simple_postprocessor", "params": {}}
        ]
    },
    "runtime_pipeline": {
        "session_manager": {"name": "simple_session_manager", "params": {}},
        "model": {"name": "openai_model", "params": {"model": "gpt-4o-mini",
        "temperature": 0.7}},
        "mode": {"name": "chat_mode", "params": {}}
    },
    "flow": [
        "data_pipeline",
        "retrieval_pipeline",
        "generation_pipeline",
        "runtime_pipeline"
    ]
}
