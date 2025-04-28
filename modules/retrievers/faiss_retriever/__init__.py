# modules/retrievers/faiss_retriever.py

import os
import faiss  # pip install faiss-cpu
import numpy as np
import pickle
from registry import ModuleRegistry

class FAISSRetriever:
    """高速検索＋永続化＋メタ情報付きRetriever（config管理版）"""

    def __init__(self, embedding_dim=128, top_k=3, index_path=None):
        self.embedding_dim = embedding_dim
        self.top_k = top_k
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.chunk_data = []  # id→{"text": str, "metadata": dict}
        self.index_path = index_path  # ★追加：indexファイルパス

        if self.index_path and self._check_index_exists():
            self.load(self.index_path)

    def _check_index_exists(self):
        return os.path.exists(f"{self.index_path}.faiss") and os.path.exists(f"{self.index_path}_chunks.pkl")

    def ingest(self, chunks, embedder):
        """チャンクリストをベクトル化＋FAISS登録"""
        if self.index_path and self._check_index_exists():
            print(f"[FAISSRetriever] Index already exists at {self.index_path}, skipping ingest.")
            return  # すでにロード済みなら何もしない

        print(f"[FAISSRetriever] Ingesting {len(chunks)} chunks...")

        vectors = []
        for chunk in chunks:
            if isinstance(chunk, dict):
                text = chunk["text"]
                metadata = chunk.get("metadata", {})
            else:
                text = chunk
                metadata = {}

            vector = embedder.embed(text)
            vectors.append(vector)
            self.chunk_data.append({"text": text, "metadata": metadata})  # ★ここ！保存形式を統一

        vectors = np.array(vectors).astype(np.float32)
        self.index.add(vectors)

        print(f"[FAISSRetriever] FAISS index size: {self.index.ntotal}")

        if self.index_path:
            self.save(self.index_path)

    def retrieve(self, query_vector, top_k=None, with_scores=False):
        """ベクトルから最近傍チャンクを取得"""
        if self.index.ntotal == 0:
            return []

        k = top_k if top_k is not None else self.top_k
        D, I = self.index.search(np.array(query_vector, dtype=np.float32).reshape(1, -1), k)

        retrieved = []
        for idx, dist in zip(I[0], D[0]):
            if idx < len(self.chunk_data):
                chunk = self.chunk_data[idx]
                if with_scores:
                    score = 1.0 / (1.0 + dist)
                    retrieved.append((chunk, score))
                else:
                    retrieved.append(chunk)

        return retrieved




    def save(self, path_prefix: str):
        """FAISSインデックスとチャンクデータを保存する"""
        os.makedirs(os.path.dirname(path_prefix), exist_ok=True)
        faiss.write_index(self.index, f"{path_prefix}.faiss")
        with open(f"{path_prefix}_chunks.pkl", "wb") as f:
            pickle.dump(self.chunk_data, f)
        print(f"[FAISSRetriever] Saved index and chunks to {path_prefix}.*")

    def load(self, path_prefix: str):
        """保存したFAISSインデックスとチャンクデータをロードする"""
        self.index = faiss.read_index(f"{path_prefix}.faiss")
        with open(f"{path_prefix}_chunks.pkl", "rb") as f:
            self.chunk_data = pickle.load(f)
        print(f"[FAISSRetriever] Loaded index and chunks from {path_prefix}.*")

# レジストリ登録
ModuleRegistry.register("faiss_retriever", FAISSRetriever)
