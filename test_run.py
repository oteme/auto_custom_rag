# test_run.py

from manager import PipelineManager
from config_for_test import config

def main():
    print("[test_run] パイプライン初期化開始...")
    manager = PipelineManager(config)
    manager.initialize_pipeline()

    print("[test_run] モード実行開始...")
    manager.mode_runner.run()

if __name__ == "__main__":
    main()
