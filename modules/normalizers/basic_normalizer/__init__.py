# modules/normalizers/basic_normalizer.py

from registry import ModuleRegistry

class BasicNormalizer:
    def __init__(self):
        pass

    def normalize(self, parsed_doc):
        print(f"[BasicNormalizer] Normalizing parsed document: {parsed_doc}")
        return f"Normalized({parsed_doc})"

# 起動時にレジストリ登録
ModuleRegistry.register("basic_normalizer", BasicNormalizer)
