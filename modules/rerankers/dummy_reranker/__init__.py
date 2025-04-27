# modules/rerankers/dummy_reranker.py

from registry import ModuleRegistry

class DummyReranker:
    def __init__(self):
        pass

    def rerank(self, chunks, query):
        print(f"[DummyReranker] Reranking chunks for query: {query}")
        # 単純にチャンクの長さ順で並び替える
        reranked = sorted(chunks, key=len)
        return reranked

# 起動時にレジストリ登録
ModuleRegistry.register("dummy_reranker", DummyReranker)
