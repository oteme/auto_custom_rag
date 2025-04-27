# modules/embedders/dummy_embedder.py

from registry import ModuleRegistry

class DummyEmbedder:
    def __init__(self):
        pass

    def embed(self, chunk):
        print(f"[DummyEmbedder] Embedding chunk: {chunk}")
        # 実際はベクトルじゃないけど、それっぽい表現
        return f"Vector({chunk})"

# 起動時にレジストリ登録
ModuleRegistry.register("dummy_embedder", DummyEmbedder)
