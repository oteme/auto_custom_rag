# test_faiss_save_load.py

from modules.retrievers.faiss_retriever import FAISSRetriever
from modules.embedders.hf_embedder import HuggingFaceEmbedder
import os

def main():
    embedder = HuggingFaceEmbedder(model_name="all-MiniLM-L6-v2")
    retriever = FAISSRetriever(embedding_dim=384, top_k=5, index_path="data/test_index")

    chunks = [
        {"text": "The Amazon rainforest is the largest tropical rainforest.", "metadata": {"source": "amazon.pdf", "page": 1}},
        {"text": "Forests play a crucial role in carbon sequestration.", "metadata": {"source": "climate.docx", "page": 2}},
        {"text": "Boreal forests are found in northern latitudes.", "metadata": {"source": "boreal.txt", "page": 5}},
        {"text": "Deforestation has major impacts on biodiversity.", "metadata": {"source": "biodiversity.pptx", "page": 3}},
        {"text": "Mangrove forests protect coastal areas from erosion.", "metadata": {"source": "coastline.pdf", "page": 7}},
    ]

    retriever.ingest(chunks, embedder)
    retriever.save("data/test_index")

    new_retriever = FAISSRetriever(embedding_dim=384, top_k=5, index_path="data/test_index")
    new_retriever.load("data/test_index")

    query = "How do forests impact climate?"
    query_vector = embedder.embed(query)
    results = new_retriever.retrieve(query_vector, with_scores=True)

    print("\n🔍 Retrieved Chunks with Metadata and Scores:")
    for chunk, score in results:
        print(f"- text: {chunk['text']}")
        print(f"  metadata: {chunk['metadata']}")
        print(f"  score: {score:.4f}")

if __name__ == "__main__":
    main()
