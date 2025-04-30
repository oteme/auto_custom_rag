from registry import ModuleRegistry
from manager  import PipelineManager
from config_for_test import config

mgr  = PipelineManager(config)
orch = config["orchestrator"]

# --- session manager だけは早い段階でインスタンス化しておく
sm_conf = orch["session_manager"]
SessionMgrCls = ModuleRegistry.get_class(sm_conf["name"])
sm = SessionMgrCls(**sm_conf.get("params", {}))

# --- dialogue controller を遅延バインド
dlg_conf = orch["dialogue_ctrl"]
DlgCls = ModuleRegistry.get_class(dlg_conf["name"])
dlg = DlgCls(manager=mgr,          # ← Manager を注入
             session_manager=sm,
             **dlg_conf.get("params", {}))

# --- UI adapter も同様
ui_conf = orch["ui_adapter"]
UICls = ModuleRegistry.get_class(ui_conf["name"])
ui = UICls(dialogue=dlg, **ui_conf.get("params", {}))

ui.run()
