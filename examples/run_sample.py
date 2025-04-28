# examples/run_sample.py
import sys
import os

# 🔥 プロジェクトルートをPythonパスに追加する！！
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manager import PipelineManager
from config_for_test import config

def main():
    print("🚀 Starting Auto-Custom-RAG Sample Run")
    
    # 1. PipelineManager作成
    manager = PipelineManager(config)
    
    # 2. パイプライン初期化
    print("\n[Step 1] Initializing pipeline...")
    manager.initialize_pipeline()
    
    # 3. データパイプライン実行（データ取り込み）
    print("\n[Step 2] Running data ingestion...")
    manager._run_data_pipeline()
    
    # 4. クエリを入力してretrievalからgenerationまで流す
    query = "Tell me about tropical rainforests"
    print(f"\n[Step 3] Processing query: '{query}'")

    retrieved_chunks = manager.retrieve_chunks(query)

    print("\n🔎 Retrieved Chunks (after merging, filtering, reranking):")
    for chunk in retrieved_chunks:
        print(f"- {chunk.get('text', chunk)} (score: {chunk.get('score', 'N/A')})")

    # 5. プロンプト生成
    prompt = manager.prompt_template.format_prompt(query, retrieved_chunks)
    print("\n📝 Generated Prompt:")
    print(prompt)

    # 6. モデル推論
    response = manager.model.generate(prompt)
    print("\n🤖 Model Response:")
    print(response)

    # 7. ポストプロセス
    for postprocessor in manager.postprocessors:
        response = postprocessor.postprocess(response)

    print("\n🎉 Final Output:")
    print(response)

if __name__ == "__main__":
    main()
