# modules/dialogue_ctrl/simple_dialogue/__init__.py
from registry import ModuleRegistry


class SimpleDialogueController:
    """
    会話履歴の管理と Manager.run_flow() 呼び出しだけを担当
    """
    def __init__(self, manager, session_manager):
        self.manager = manager
        self.sm = session_manager
        try:
            self.flow = manager.config["orchestrator"]["flow"]
        except KeyError as e:
            raise ValueError(
                "config.orchestrator.flow が未定義です。"
                " DialogueController を作る前に必ず設定してください。"
            ) from e

    def handle(self, user_msg: str) -> str:
        self.sm.add_message("user", user_msg)

        answer = self.manager.run_flow(self.flow, query=user_msg)

        self.sm.add_message("assistant", answer)
        return answer


ModuleRegistry.register("simple_dialogue", SimpleDialogueController)
