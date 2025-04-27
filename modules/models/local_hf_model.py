# modules/models/local_hf_model.py

from __future__ import annotations

import os
from typing import Optional

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline  # pip install transformers accelerate
from registry import ModuleRegistry


class LocalHFModel:
    """Run a HF model fully locally (CPU/GPU)."""

    def __init__(self, model_name: str = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
                 device: str | int = "cuda:0" if os.getenv("CUDA_VISIBLE_DEVICES") else "cpu",
                 max_new_tokens: int = 512,
                 temperature: float = 0.0,
                 **generate_kwargs):
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
        self._pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device=device)
        self.generate_kwargs = {"max_new_tokens": max_new_tokens, "temperature": temperature, **generate_kwargs}

    def generate(self, prompt: str) -> str:
        out = self._pipe(prompt, **self.generate_kwargs)[0]["generated_text"]
        return out.strip()


ModuleRegistry.register("local_hf_model", LocalHFModel)