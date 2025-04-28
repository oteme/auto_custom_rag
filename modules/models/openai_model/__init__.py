# modules/models/openai_model.py

import os
from dotenv import load_dotenv
import openai
from registry import ModuleRegistry

# 環境変数ロード
load_dotenv()

class OpenAIModel:
    def __init__(self, model="gpt-4o", temperature=0.0, **kwargs):
        """
        paramsには以下が渡せる
          - api_key（優先）
          - azure_api_key / azure_api_base / azure_api_version（Azure用）
          - その他OpenAI API用パラメータ
        """
        # paramsから受け取る
        api_key         = kwargs.pop("api_key", None)
        azure_api_key   = kwargs.pop("azure_api_key", None)
        azure_api_base  = kwargs.pop("azure_api_base", None)
        azure_api_version = kwargs.pop("azure_api_version", "2023-12-01-preview")
        use_azure       = kwargs.pop("use_azure", False)

        # まずは通常OpenAI APIを優先
        if (api_key or os.getenv("OPENAI_API_KEY")) and not use_azure:
            openai.api_key = api_key or os.getenv("OPENAI_API_KEY")
            self._client = openai.Client()
            self.mode = "openai"
        # それがダメならAzure OpenAIに切り替える
        elif (azure_api_key or os.getenv("AOAI_API_KEY")):
            openai.AzureOpenAI.api_key = azure_api_key or os.getenv("AOAI_API_KEY")
            openai.AzureOpenAI.api_base = azure_api_base or os.getenv("AOAI_API_BASE")
            openai.AzureOpenAI.api_version = azure_api_version or os.getenv("AOAI_API_VERSION", "2023-12-01-preview")
            self._client = openai.AzureOpenAI()
            self.mode = "azure"
        else:
            raise ValueError("No valid OpenAI or Azure OpenAI API credentials provided.")

        self.model = model
        self.temperature = temperature
        self.completion_kwargs = kwargs

    def generate(self, prompt: str) -> str:
        """ プロンプトを送って応答を得る """
        resp = self._client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            **self.completion_kwargs,
        )
        return resp.choices[0].message.content.strip()


# モジュール登録
ModuleRegistry.register("openai_model", OpenAIModel)
