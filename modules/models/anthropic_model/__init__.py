# modules/models/anthropic_model.py

import os
from dotenv import load_dotenv
from registry import ModuleRegistry
import anthropic  # pip install anthropic

# .env読み込み
load_dotenv()

class AnthropicModel:
    """Anthropic Claude系モデル呼び出し用ラッパー"""

    def __init__(self, model="claude-3-opus-20240229", temperature=0.0, max_tokens=1024, **kwargs):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set in .env")

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.generate_kwargs = kwargs

    def generate(self, prompt: str) -> str:
        """プロンプトを投げて、Claude応答を受け取る"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[
                {"role": "user", "content": prompt}
            ],
            **self.generate_kwargs,
        )
        return response.content[0].text.strip()

# モジュールレジストリ登録
ModuleRegistry.register("anthropic_model", AnthropicModel)
