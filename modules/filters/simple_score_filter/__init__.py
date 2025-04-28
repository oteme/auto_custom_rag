# modules/filters/simple_score_filter/__init__.py

from registry import ModuleRegistry

class SimpleScoreFilter:
    def __init__(self, threshold=0.5):
        self.threshold = threshold

    def filter(self, chunks_with_scores, query=None):
        """スコアがthreshold以上のチャンクだけ残す"""
        print(f"[SimpleScoreFilter] Filtering by score threshold: {self.threshold}")

        filtered = []
        for item in chunks_with_scores:
            if isinstance(item, tuple) and len(item) == 2:
                chunk, score = item
                if score >= self.threshold:
                    filtered.append(chunk)  # スコアはdiscardしてチャンクだけ残す
            else:
                filtered.append(item)  # スコア情報なければそのまま通す

        return filtered

# 登録
ModuleRegistry.register("simple_score_filter", SimpleScoreFilter)
