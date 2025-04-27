# modules/parsers/simple_parser.py

from registry import ModuleRegistry

class SimpleParser:
    def __init__(self):
        pass

    def parse(self, raw_doc):
        print(f"[SimpleParser] Parsing document: {raw_doc}")
        return f"Parsed({raw_doc})"

# 起動時にレジストリ登録
ModuleRegistry.register("simple_parser", SimpleParser)
