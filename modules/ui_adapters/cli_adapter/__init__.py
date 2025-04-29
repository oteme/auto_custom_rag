# modules/ui_adapters/cli_adapter/__init__.py
from registry import ModuleRegistry

class CLIAdapter:
    def __init__(self, manager, dialogue, **_):
        self.dialogue = dialogue

    def run(self):
        print("💬 CLI (exit で終了)")
        while True:
            msg = input("🧑: ")
            if msg.lower() in {"exit", "quit"}:
                break
            ans = self.dialogue.handle(msg)
            print("🤖:", ans)

ModuleRegistry.register("cli_adapter", CLIAdapter)
