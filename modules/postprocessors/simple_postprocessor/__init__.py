# modules/postprocessors/simple_postprocessor.py

from registry import ModuleRegistry

class SimplePostProcessor:
    def __init__(self):
        pass

    def postprocess(self, response):
        print(f"[SimplePostProcessor] Postprocessing the response")
        return f"【回答】\n{response.strip()}"

ModuleRegistry.register("simple_postprocessor", SimplePostProcessor)
