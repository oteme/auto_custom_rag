# modules/filters/simple_filter.py

from registry import ModuleRegistry

class SimpleFilter:
    def __init__(self):
        pass

    def filter(self, chunks, query):
        print(f"[SimpleFilter] Filtering chunks for query: {query}")
        keyword = query.lower()

        filtered = []
        for chunk in chunks:
            text = chunk["text"] if isinstance(chunk, dict) else chunk
            if keyword in text.lower():
                filtered.append(chunk)

        if not filtered:
            return chunks  # 全部落ちるのを防ぐ
        return filtered

ModuleRegistry.register("simple_filter", SimpleFilter)
