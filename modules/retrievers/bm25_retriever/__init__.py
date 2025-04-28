# modules/retrievers/bm25_retriever/__init__.py

from registry import ModuleRegistry
from rank_bm25 import BM25Okapi  # pip install rank-bm25
import re

class BM25Retriever:
    def __init__(self, top_k=3):
        self.top_k = top_k
        self.corpus = []
        self.chunk_texts = []
        self.bm25 = None

    def ingest(self, chunks, embedder=None):
        """チャンクリストを取り込んでBM25インデックスを作る"""
        print(f"[BM25Retriever] Ingesting {len(chunks)} chunks...")
        for chunk in chunks:
            text = chunk["text"] if isinstance(chunk, dict) else chunk
            tokens = self._tokenize(text)
            self.corpus.append(tokens)
            self.chunk_texts.append(chunk)

        self.bm25 = BM25Okapi(self.corpus)

    def retrieve(self, query):
        """クエリに対してBM25検索を行う"""
        if not self.bm25:
            raise ValueError("[BM25Retriever] No corpus indexed. Call ingest() first.")

        query_tokens = self._tokenize(query)
        scores = self.bm25.get_scores(query_tokens)

        ranked = sorted(zip(scores, self.chunk_texts), reverse=True)
        top_chunks = [chunk for _, chunk in ranked[:self.top_k]]

        return top_chunks

    def _tokenize(self, text):
        """簡易トークナイザー"""
        return re.findall(r'\w+', text.lower())

# モジュール登録
ModuleRegistry.register("bm25_retriever", BM25Retriever)
