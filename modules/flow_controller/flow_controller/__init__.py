class FlowController:
    def __init__(self):
        self.flows = {}
        self.current_flow = None

    def add_flow(self, name, config):
        """新しいフローを追加する"""
        self.flows[name] = config

    def set_current_flow(self, name):
        """現在使うフローを切り替える"""
        if name not in self.flows:
            raise ValueError(f"Flow '{name}' not registered.")
        self.current_flow = self.flows[name]

    def get_current_flow(self):
        """現在アクティブなフローを返す"""
        if not self.current_flow:
            raise ValueError("No current flow selected.")
        return self.flows[self.current_flow]
