import os
from dotenv import load_dotenv
from registry import ModuleRegistry
import openai

load_dotenv()

class OpenAIModel:
    def __init__(self, model="gpt-4o", temperature=0.0, **kwargs):
        # Azure APIを使用するフラグ - デフォルトではFalseに設定
        use_azure = kwargs.pop('use_azure', False)
        
        if use_azure and os.getenv("AOAI_API_BASE"):  # Azure OpenAIを明示的に指定した場合のみ
            openai.AzureOpenAI.api_key = os.getenv("AOAI_API_KEY")
            openai.AzureOpenAI.api_base = os.getenv("AOAI_API_BASE")
            openai.AzureOpenAI.api_version = os.getenv("AOAI_API_VERSION", "2023-12-01-preview")
            self._client = openai.AzureOpenAI()
        else:  # 標準のOpenAI
            openai.api_key = os.getenv("OPENAI_API_KEY")
            self._client = openai.Client()
        
        self.model = model
        self.temperature = temperature
        self.completion_kwargs = kwargs

    def generate(self, prompt: str) -> str:
        resp = self._client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            **self.completion_kwargs,
        )
        return resp.choices[0].message.content.strip()

ModuleRegistry.register("openai_model", OpenAIModel)
