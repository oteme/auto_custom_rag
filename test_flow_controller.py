# test_flow_controller.py

from flow_controller import FlowController

def main():
    fc = FlowController()

    # 仮flowを登録
    sample_flow = {
        "steps": [
            {"type": "embedder", "name": "sample_embedder"},
            {"type": "retriever", "name": "sample_retriever"}
        ]
    }
    fc.register_flow("sample_chat", sample_flow)

    # 選択
    fc.select_flow("sample_chat")

    # 取得
    current = fc.get_current_flow()

    print("✅ Selected Flow Config:")
    print(current)

if __name__ == "__main__":
    main()
