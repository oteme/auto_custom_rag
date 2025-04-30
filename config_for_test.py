config = {
    "pipelines": {
        "data": {
            "steps": [
                {"type": "loader", "name": "pdf_loader",
                                "params": {"path": "data/pdfs/"}},
                {"type": "parser", "name": "simple_parser"},
                {"type": "normalizer", "name": "basic_normalizer"},
                {"type": "chunker", "name": "simple_chunker"}
            ]
        },
        "retrieval": {
            "steps": [
                {"type": "embedder", "name": "hf_embedder",
                                   "params": {"model_name": "all-MiniLM-L6-v2"}},
                {"type": "retriever", "name": "faiss_retriever",
                                     "params": {"embedding_required": True,
                                                "embedding_dim": 384,
                                                "top_k": 5}},
                {"type": "filter", "name": "simple_score_filter",
                                   "params": {"threshold": 0.5}},
                {"type": "filter", "name": "metadata_filter",
                                   "params": {"key": "source",
                                              "allowed_values": ["important_doc1.pdf",
                                                                 "important_doc2.pdf"]}},
                {"type": "reranker", "name": "simple_reranker"}
            ]
        },
        "generation": {
            "steps": [
                {"type": "prompt_template", "name": "simple_prompt_template"},
                {"type": "model", "name": "openai_model",
                                 "params": {"model": "gpt-4o-mini",
                                            "temperature": 0.7}},
                {"type": "postprocessor", "name": "simple_postprocessor"}
            ]
        }
    },
    "orchestrator": {
        "flow": ["data", "retrieval", "generation"],
        "session_manager": {"name": "simple_session_manager"},
        "dialogue_ctrl"  : {"name": "simple_dialogue"},
        "ui_adapter"     : {"name": "cli_adapter"}
    }
}
