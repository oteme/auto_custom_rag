from registry import ModuleRegistry

class ScoreMaxMerge:
    def __init__(self):
        pass

    def merge(self, chunks_list):
        best_chunks = {}
        for chunk in chunks_list:
            text = chunk["text"] if isinstance(chunk, dict) else chunk
            score = chunk.get("score", 0) if isinstance(chunk, dict) else 0
            if text not in best_chunks or score > best_chunks[text].get("score", -float('inf')):
                best_chunks[text] = chunk
        return list(best_chunks.values())

ModuleRegistry.register("score_max_merge", ScoreMaxMerge)
