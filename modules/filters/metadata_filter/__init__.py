# modules/filters/metadata_filter/__init__.py

from registry import ModuleRegistry

class MetadataFilter:
    def __init__(self, key, allowed_values):
        """
        key: メタデータのキー名（例: "source"）
        allowed_values: 許可する値リスト（例: ["doc1.pdf", "doc2.pdf"]）
        """
        self.key = key
        self.allowed_values = allowed_values

    def filter(self, chunks, query=None):
        filtered = []
        for chunk in chunks:
            metadata = chunk.get("metadata", {}) if isinstance(chunk, dict) else {}
            if metadata.get(self.key) in self.allowed_values:
                filtered.append(chunk)

        return filtered if filtered else chunks  # 0件にならないようfallback

# モジュール登録
ModuleRegistry.register("metadata_filter", MetadataFilter)
