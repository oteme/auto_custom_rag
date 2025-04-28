from registry import ModuleRegistry

class UniqueMerge:
    def __init__(self):
        pass

    def merge(self, chunks_list):
        seen = set()
        unique_chunks = []
        for chunk in chunks_list:
            text = chunk["text"] if isinstance(chunk, dict) else chunk
            if text not in seen:
                seen.add(text)
                unique_chunks.append(chunk)
        return unique_chunks

ModuleRegistry.register("unique_merge", UniqueMerge)
