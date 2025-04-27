# config_for_test.py

config = {
    "data_pipeline": {
        "loaders": [
            "pdf_loader"
        ],
        "parser": "simple_parser",
        "normalizer": "basic_normalizer",
        "chunker": "simple_chunker",
        "embedder": "simple_embedder"
    },
    "retrieval_pipeline": {
        "retriever": "simple_retriever",
        "filters": [
            "simple_filter"
        ],
        "reranker": "simple_reranker"
    },
    "generation_pipeline": {
        "prompt_template": "simple_prompt_template",
        "postprocessors": [
            "simple_postprocessor"
        ]
    }
}
