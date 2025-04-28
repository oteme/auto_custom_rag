# modules/retrieval_mergers/simple_merge/__init__.py

from registry import ModuleRegistry

class SimpleMerge:
    def __init__(self, strategy="concat"):
        self.strategy = strategy

    def merge(self, chunks_list):
        if self.strategy == "concat":
            return chunks_list

        elif self.strategy == "unique":
            seen = set()
            unique_chunks = []
            for chunk in chunks_list:
                text = chunk["text"] if isinstance(chunk, dict) else chunk
                if text not in seen:
                    seen.add(text)
                    unique_chunks.append(chunk)
            return unique_chunks

        else:
            raise ValueError(f"Unknown merge strategy: {self.strategy}")

# モジュール登録
ModuleRegistry.register("simple_merge", SimpleMerge)
