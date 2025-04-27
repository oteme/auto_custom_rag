# modules/rerankers/simple_reranker.py

from registry import ModuleRegistry

class SimpleReranker:
    def __init__(self):
        pass

    def rerank(self, chunks, query):
        print(f"[SimpleReranker] Reranking chunks for query: {query}")

        # チャンクの長さ順に並べ替え（テキスト部分を見る）
        sorted_chunks = sorted(
            chunks,
            key=lambda chunk: len(chunk["text"]) if isinstance(chunk, dict) else len(chunk)
        )
        return sorted_chunks

ModuleRegistry.register("simple_reranker", SimpleReranker)
