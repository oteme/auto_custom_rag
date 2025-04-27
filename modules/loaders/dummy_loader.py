# modules/loaders/dummy_loader.py

from registry import ModuleRegistry

class DummyLoader:
    def __init__(self, path=None):
        self.path = path  # ダミーなので使わない

    def load(self):
        print(f"[DummyLoader] Loading dummy documents from {self.path}")
        return [
            "This is a dummy document about forests.",
            "Another dummy document about oceans.",
            "Yet another dummy document about mountains."
        ]

# 起動時にレジストリ登録
ModuleRegistry.register("dummy_loader", DummyLoader)
