# modules/models/local_hf_model.py

from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch
from registry import ModuleRegistry

class LocalHFModel:
    def __init__(self, model_path="gpt2", device=None, temperature=0.7, **kwargs):
        """
        model_path: ローカルまたはHuggingFace Hubのモデル名
        device: None=自動選択 (cuda優先) / "cuda" / "cpu"
        """
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path).to(self.device)
        self.temperature = temperature
        self.generation_kwargs = kwargs

    def generate(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            do_sample=True,
            temperature=self.temperature,
            max_new_tokens=500,
            **self.generation_kwargs
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

ModuleRegistry.register("local_hf_model", LocalHFModel)
