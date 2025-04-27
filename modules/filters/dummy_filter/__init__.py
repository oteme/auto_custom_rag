# modules/filters/dummy_filter.py

from registry import ModuleRegistry

class DummyFilter:
    def __init__(self):
        pass

    def filter(self, chunks, query):
        print(f"[DummyFilter] Filtering chunks for query: {query}")
        # クエリに "tree" を含んでたら、それっぽいチャンクだけ残す
        filtered = [chunk for chunk in chunks if "tree" in chunk.lower()]
        return filtered if filtered else chunks  # 一応全部落ちないように

# 起動時にレジストリ登録
ModuleRegistry.register("dummy_filter", DummyFilter)
