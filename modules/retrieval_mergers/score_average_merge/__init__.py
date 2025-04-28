from registry import ModuleRegistry

class ScoreAverageMerge:
    def __init__(self):
        pass

    def merge(self, chunks_list):
        score_map = {}
        count_map = {}
        chunk_map = {}
        for chunk in chunks_list:
            text = chunk["text"] if isinstance(chunk, dict) else chunk
            score = chunk.get("score", 0) if isinstance(chunk, dict) else 0
            if text not in score_map:
                score_map[text] = 0
                count_map[text] = 0
                chunk_map[text] = chunk
            score_map[text] += score
            count_map[text] += 1

        averaged_chunks = []
        for text, total_score in score_map.items():
            chunk = chunk_map[text]
            avg_score = total_score / count_map[text]
            chunk["score"] = avg_score
            averaged_chunks.append(chunk)
        return averaged_chunks

ModuleRegistry.register("score_average_merge", ScoreAverageMerge)
