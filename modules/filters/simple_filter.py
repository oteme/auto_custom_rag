# modules/filters/simple_filter.py

from registry import ModuleRegistry

class SimpleFilter:
    def __init__(self):
        pass

    def filter(self, chunks, query):
        print(f"[SimpleFilter] Filtering chunks for query: {query}")
        keyword = query.lower()
        filtered = [chunk for chunk in chunks if keyword in chunk.lower()]
        if not filtered:
            return chunks  # 全部落ちるのは避ける
        return filtered

ModuleRegistry.register("simple_filter", SimpleFilter)
