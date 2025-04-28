# modules/modes/chat_mode.py

from registry import ModuleRegistry

class ChatMode:
    def __init__(self, manager, **kwargs):
        self.manager = manager
        self.history = []

    def run(self):
        print("💬 Chat Mode Activated! (type 'exit' to quit)")
        
        while True:
            user_query = input("🧑‍💻 You: ")
            if user_query.strip().lower() == "exit":
                print("👋 Goodbye!")
                break

            # Append user query to history
            self.history.append({"role": "user", "content": user_query})

            # Retrieval
            retrieved_chunks = self.manager.retrieve_chunks(user_query)

            # Prompt Generation (履歴込みで作るならカスタマイズ可能)
            prompt = self.manager.prompt_template.format_prompt(user_query, retrieved_chunks)

            # Model Inference
            response = self.manager.model.generate(prompt)

            # Append model response to history
            self.history.append({"role": "assistant", "content": response})

            # Postprocess
            for postprocessor in self.manager.postprocessors:
                response = postprocessor.postprocess(response)

            print("\n🤖 Assistant:")
            print(response)

ModuleRegistry.register("chat_mode", ChatMode)
