# config_for_test.py

config = {
    "data_pipeline": {
        "loaders": [
            {"name": "pdf_loader", "params": {"path": "data/pdfs/"}}
        ],
        "parser": {"name": "simple_parser", "params": {}},
        "normalizer": {"name": "basic_normalizer", "params": {}},
        "chunker": {"name": "simple_chunker", "params": {}},
        "embedder": {"name": "simple_embedder", "params": {"embedding_dim": 128}}
    },
    "retrieval_pipeline": {
        "steps": [
            {"type": "retriever", "name": "simple_retriever", "params": {}},
            {"type": "filter", "name": "simple_filter", "params": {}},
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
