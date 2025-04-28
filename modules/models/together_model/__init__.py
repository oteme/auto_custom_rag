# modules/models/together_model.py

import os
from dotenv import load_dotenv
import together
from registry import ModuleRegistry

load_dotenv()

class TogetherModel:
    def __init__(self, model="togethercomputer/llama-2-7b-chat", temperature=0.7, **kwargs):
        api_key = kwargs.pop("api_key", None) or os.getenv("TOGETHER_API_KEY")

        if not api_key:
            raise ValueError("TOGETHER_API_KEY must be set via params or .env file.")

        together.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.generation_kwargs = kwargs

    def generate(self, prompt: str) -> str:
        response = together.Complete.create(
            prompt=prompt,
            model=self.model,
            temperature=self.temperature,
            **self.generation_kwargs
        )
        return response["output"]["choices"][0]["text"].strip()

ModuleRegistry.register("together_model", TogetherModel)
