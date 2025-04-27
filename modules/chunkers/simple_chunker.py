# modules/chunkers/simple_chunker.py

from registry import ModuleRegistry

class SimpleChunker:
    def __init__(self):
        pass

    def chunk(self, normalized_doc):
        print(f"[SimpleChunker] Chunking normalized document: {normalized_doc}")
        # ダミーで2チャンクに分ける
        return [
            f"Chunk1({normalized_doc})",
            f"Chunk2({normalized_doc})"
        ]

# 起動時にレジストリ登録
ModuleRegistry.register("simple_chunker", SimpleChunker)
