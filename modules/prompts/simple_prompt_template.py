# modules/prompts/simple_prompt_template.py

from registry import ModuleRegistry

class SimplePromptTemplate:
    def __init__(self):
        pass

    def format_prompt(self, query, context_chunks):
        print(f"[SimplePromptTemplate] Formatting prompt for query: {query}")
        
        context_texts = [
            chunk["text"] if isinstance(chunk, dict) else chunk
            for chunk in context_chunks
        ]
        context = "\n".join(context_texts)

        prompt = (
            f"Use the following context to answer the question:\n"
            f"{context}\n\n"
            f"Question: {query}"
        )
        return prompt

ModuleRegistry.register("simple_prompt_template", SimplePromptTemplate)
