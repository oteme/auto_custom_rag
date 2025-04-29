try:
    from slack_sdk.socket_mode import SocketModeClient
    from slack_sdk.web import WebClient
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False

class SlackAdapter:
    """Slack Socket‑Mode アダプタ (参考)"""

    def __init__(self, manager, bot_token: str, app_token: str):
        if not SLACK_AVAILABLE:
            raise RuntimeError("slack_sdk 未インストールです")
        self.manager = manager
        self.client = SocketModeClient(app_token=app_token, web_client=WebClient(token=bot_token))

    def run(self):
        flow = self.manager.config["flow"]

        @self.client.socket_mode_request_listeners.append
        def handle(event):
            if event.type != "events_api":
                return
            payload = event.payload["event"]
            if payload.get("bot_id"):
                return  # 自分の発言は無視
            text = payload.get("text", "")
            channel = payload["channel"]
            answer = self.manager.run_flow(flow, query=text)
            self.client.web_client.chat_postMessage(channel=channel, text=answer)
            self.client.ack(event)

        self.client.connect()
        self.client.start()

ModuleRegistry.register("slack_adapter", SlackAdapter)