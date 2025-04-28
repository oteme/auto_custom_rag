# modules/models/anthropic_model.py

import os
from dotenv import load_dotenv
import anthropic
from registry import ModuleRegistry

load_dotenv()

class AnthropicModel:
    def __init__(self, model="claude-3-opus-20240229", temperature=0.7, **kwargs):
        api_key = kwargs.pop("api_key", None) or os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set via params or .env file.")

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.generation_kwargs = kwargs

    def generate(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}],
            **self.generation_kwargs
        )
        return response.content[0].text.strip()

ModuleRegistry.register("anthropic_model", AnthropicModel)
