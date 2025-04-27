# modules/models/together_model.py

import os
from dotenv import load_dotenv
from registry import ModuleRegistry
import together  # pip install together

# .env読み込み
load_dotenv()

class TogetherModel:
    """Together.aiのモデル呼び出しラッパー"""

    def __init__(self, model="mistralai/Mistral-7B-Instruct-v0.2", temperature=0.0, max_tokens=1024, **kwargs):
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            raise ValueError("TOGETHER_API_KEY is not set in .env")

        together.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.generate_kwargs = kwargs

    def generate(self, prompt: str) -> str:
        """プロンプトを投げてTogether.ai経由で推論する"""
        response = together.Complete.create(
            model=self.model,
            prompt=prompt,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            **self.generate_kwargs,
        )
        return response["output"]["choices"][0]["text"].strip()

# モジュールレジストリ登録
ModuleRegistry.register("together_model", TogetherModel)
