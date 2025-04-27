# registry.py

import importlib

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
        # どのカテゴリに属するか推測する
        for category in ["loaders", "parsers", "normalizers", "chunkers", "embedders",
                        "retrievers", "filters", "rerankers", "prompts", "postprocessors", "models"]:
            try:
                importlib.import_module(f"modules.{category}.{name}")
                print(f"[Registry] Dynamically imported modules.{category}.{name}")
                return
            except ModuleNotFoundError:
                continue
