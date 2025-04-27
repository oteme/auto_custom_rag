# modules/retrievers/simple_retriever.py

import numpy as np
from scipy.spatial.distance import cosine
from registry import ModuleRegistry

class SimpleRetriever:
    def __init__(self):
        self.chunk_vectors = []  # ベクトルリスト
        self.chunk_texts = []    # 元チャンクリスト

    def ingest(self, chunks, embedder):
        print(f"[SimpleRetriever] Ingesting {len(chunks)} chunks...")
        for chunk in chunks:
            vector = embedder.embed(chunk)
            self.chunk_vectors.append(vector)
            self.chunk_texts.append(chunk)

    def retrieve(self, query):
        print(f"[SimpleRetriever] Retrieving for query: {query}")
        if not self.chunk_vectors:
            return []

        # クエリ自体を埋め込み（単純にランダムで）
        query_vector = np.random.rand(len(self.chunk_vectors[0]))

        # コサイン類似度でスコア計算
        scores = []
        for idx, vec in enumerate(self.chunk_vectors):
            score = 1 - cosine(query_vector, vec)  # コサイン類似度
            scores.append((score, self.chunk_texts[idx]))

        # スコア順に並び替え
        scores.sort(reverse=True)

        # 上位3件だけ返す（仮）
        top_chunks = [chunk for _, chunk in scores[:3]]
        return top_chunks

# 起動時にレジストリ登録
ModuleRegistry.register("simple_retriever", SimpleRetriever)
