# registry.py

import importlib
import os
import yaml

class ModuleRegistry:
    _registry = {}

    @classmethod
    def register(cls, name, module_class):
        cls._registry[name] = module_class
        print(f"[Registry] Registered module: {name}")

    @classmethod
    def get_class(cls, name):
        if name not in cls._registry:
            print(f"[Registry] Module {name} not found. Attempting dynamic import...")
            cls._dynamic_import(name)
            if name not in cls._registry:
                raise ValueError(f"Module {name} still not found after dynamic import.")
        return cls._registry[name]

    @classmethod
    def _dynamic_import(cls, name):
        for category in [
            "loaders", "parsers", "normalizers", "chunkers", "embedders",
            "retrievers", "filters", "rerankers", "prompts", "postprocessors", "models"
        ]:
            try:
                # ←★ ここ注意
                module_path = f"modules.{category}.{name}"
                importlib.import_module(module_path)
                print(f"[Registry] Dynamically imported {module_path}")
                return
            except ModuleNotFoundError:
                continue

    @classmethod
    def get_metadata(cls, name):
        """指定したモジュール名に対応するmanifest.yamlを辞書で返す"""
        for category in [
            "loaders", "parsers", "normalizers", "chunkers", "embedders",
            "retrievers", "filters", "rerankers", "prompts", "postprocessors", "models"
        ]:
            manifest_path = os.path.join("modules", category, name, "manifest.yaml")
            if os.path.exists(manifest_path):
                with open(manifest_path, "r", encoding="utf-8") as f:
                    metadata = yaml.safe_load(f)
                    print(f"[Registry] Loaded manifest for {name}")
                    return metadata
        raise FileNotFoundError(f"Manifest for module {name} not found.")
