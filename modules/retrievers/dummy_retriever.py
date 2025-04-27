# modules/retrievers/dummy_retriever.py

from registry import ModuleRegistry

class DummyRetriever:
    def __init__(self):
        pass

    def retrieve(self, query):
        print(f"[DummyRetriever] Retrieving for query: {query}")
        # クエリに関係なく、適当なチャンクリストを返す
        return [
            "Chunk about forests",
            "Chunk about oceans",
            "Chunk about mountains"
        ]

# 起動時にレジストリ登録
ModuleRegistry.register("dummy_retriever", DummyRetriever)
