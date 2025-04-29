from registry import ModuleRegistry
from manager  import PipelineManager
from config_for_test   import config


def main():
    # ① エンジン
    mgr = PipelineManager(config)

    # ② DialogueController
    dc_conf = config["runtime_pipeline"]["dialogue_ctrl"]
    DCClass = ModuleRegistry.get_class(dc_conf["name"])
    sm_name = config["runtime_pipeline"]["session_manager"]["name"]
    session_mgr = mgr._module_cache[sm_name]
    dialogue = DCClass(mgr, session_mgr, **dc_conf.get("params", {}))

    # ③ UI Adapter（Dialogue インスタンスを注入）
    ui_conf = config["runtime_pipeline"]["ui_adapter"]
    UIClass = ModuleRegistry.get_class(ui_conf["name"])
    ui_runner = UIClass(manager=mgr, dialogue=dialogue, **ui_conf.get("params", {}))
    ui_runner.run()


if __name__ == "__main__":
    main()
