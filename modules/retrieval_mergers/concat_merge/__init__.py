from registry import ModuleRegistry

class ConcatMerge:
    def __init__(self):
        pass

    def merge(self, chunks_list):
        return chunks_list

ModuleRegistry.register("concat_merge", ConcatMerge)
