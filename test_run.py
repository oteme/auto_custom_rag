from manager import PipelineManager
from registry import ModuleRegistry
from config_for_test import config

def main():
    manager = PipelineManager(config)                 # ❶ エンジンを生成

    # ❷ config からモード定義を取り出す
    mode_conf  = config["runtime_pipeline"]["mode"]
    ModeClass  = ModuleRegistry.get_class(mode_conf["name"])

    # ❸ モードをインスタンス化（Manager を注入）
    mode_runner = ModeClass(manager=manager, **mode_conf.get("params", {}))

    # ❹ UI ループ開始
    mode_runner.run()

if __name__ == "__main__":
    main()
