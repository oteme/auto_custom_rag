# test_run.py

"""
auto-custom-rag 簡単実行サンプル

- config_for_test.pyで指定されたモジュール構成に従って
- パイプラインを初期化
- ドキュメントをインジェスト
- ユーザークエリに対して検索＆応答生成
"""

from manager import PipelineManager
from config_for_test import config

def main():
    print("[test_run] パイプライン初期化開始...")
    manager = PipelineManager(config)
    manager.initialize_pipeline()

    print("[test_run] ドキュメントインジェスト開始...")
    manager.ingest()

    print("[test_run] クエリ実行開始...")
    user_query = "Tell me about forests"
    manager.query(user_query)

if __name__ == "__main__":
    main()
