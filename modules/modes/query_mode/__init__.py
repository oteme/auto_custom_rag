# modules/modes/query_mode.py

from registry import ModuleRegistry

class QueryMode:
    def __init__(self, manager, **kwargs):
        self.manager = manager
        self.history = []  # 将来履歴使いたいとき用に一応持っておく

    def run(self):
        user_query = input("🔎 Enter your query: ")

        # Retrieval
        retrieved_chunks = self.manager.retrieve_chunks(user_query)

        # Prompt Generation
        prompt = self.manager.prompt_template.format_prompt(user_query, retrieved_chunks)

        # Model Inference
        response = self.manager.model.generate(prompt)

        # Postprocess
        for postprocessor in self.manager.postprocessors:
            response = postprocessor.postprocess(response)

        print("\n✨ Final Response ✨")
        print(response)

ModuleRegistry.register("query_mode", QueryMode)
