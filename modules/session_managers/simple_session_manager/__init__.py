# modules/session_managers/simple_session_manager.py

from registry import ModuleRegistry

class SimpleSessionManager:
    def __init__(self, **params):
        self.history = []  # 会話履歴リスト

    def add_message(self, role: str, content: str):
        """ユーザーまたはAIのメッセージを履歴に追加"""
        self.history.append({"role": role, "content": content})

    def get_context(self) -> list:
        """現在の履歴を返す（プロンプトに使うため）"""
        return self.history

    def reset(self):
        """履歴をリセット"""
        self.history = []

# 起動時にレジストリ登録
ModuleRegistry.register("simple_session_manager", SimpleSessionManager)
