# config_for_test.py
config = {
    "data_pipeline": {
        "loaders": ["pdf_loader"],
        "parser": "simple_parser",
        "normalizer": "basic_normalizer",
        "chunker": "simple_chunker",
        "embedder": "simple_embedder",
    },
    "retrieval_pipeline": {
        "retriever": "faiss_retriever",
        "filters": ["simple_filter"],
        "reranker": "simple_reranker",
    },
    "generation_pipeline": {
        "prompt_template": "simple_prompt_template",
        "postprocessors": ["simple_postprocessor"],
    },
    # ★ NEW: モデル層
    "model": {
        # "name": "openai_model",  # または "local_hf_model"
        "name": "openai_model",
        "params": {
            "model": "gpt-4o-mini",  # ご自由に
            "temperature": 0.2,
        },
    },
}