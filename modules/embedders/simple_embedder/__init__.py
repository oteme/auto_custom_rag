# modules/embedders/simple_embedder.py

import numpy as np
from registry import ModuleRegistry

class SimpleEmbedder:
    def __init__(self, embedding_dim=128, seed=42):
        self.embedding_dim = embedding_dim
        np.random.seed(seed)

    def embed(self, chunk):
        print(f"[SimpleEmbedder] Embedding chunk: {chunk}")
        # シンプルにランダムなベクトルを返す
        return np.random.rand(self.embedding_dim).tolist()

# 起動時にレジストリ登録
ModuleRegistry.register("simple_embedder", SimpleEmbedder)
