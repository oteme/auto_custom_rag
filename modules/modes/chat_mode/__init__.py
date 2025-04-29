# modules/modes/chat_mode/__init__.py
# ------------------------------------------------------------
# ChatMode ＝ もはや Interaction だけ
#  * 入力: stdin
#  * 出力: stdout
#  * 1 行入力ごとに DialogueController.handle を呼ぶ
# ------------------------------------------------------------
from registry import ModuleRegistry


class ChatMode:
    def __init__(
        self,
        manager,
        dialogue_controller: str = "simple_dialogue"  # ← config で差し替え可
    ):
        DC = ModuleRegistry.get_class(dialogue_controller)
        # SessionManager は Manager が初期化済みのものを取り出す
        sm = manager._module_cache["simple_session_manager"]
        self.dialog = DC(manager, sm)

    def run(self):
        print("💬 Chat CLI (exit で終了)")
        while True:
            msg = input("🧑: ")
            if msg.lower() in {"exit", "quit"}:
                break
            ans = self.dialog.handle(msg)
            print("🤖:", ans)
