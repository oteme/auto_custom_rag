# modules/rerankers/simple_reranker.py

from registry import ModuleRegistry

class SimpleReranker:
    def __init__(self):
        pass

    def rerank(self, chunks, query):
        print(f"[SimpleReranker] Reranking chunks for query: {query}")
        return sorted(chunks, key=len)

ModuleRegistry.register("simple_reranker", SimpleReranker)
