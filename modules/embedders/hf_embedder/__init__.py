# modules/embedders/hf_embedder/__init__.py

from sentence_transformers import SentenceTransformer
from registry import ModuleRegistry

class HuggingFaceEmbedder:
    def __init__(self, model_name="all-MiniLM-L6-v2", device=None, use_cache=True):
        """
        model_name: 使用するHuggingFace埋め込みモデル名
        device: Noneなら自動選択（cuda優先）、明示的に"cpu"や"cuda:0"なども指定可能
        use_cache: Trueなら埋め込みキャッシュを有効化する
        """
        self.model_name = model_name
        self.device = device
        self.use_cache = use_cache
        self.model = SentenceTransformer(model_name, device=device)

        self._cache = {} if use_cache else None

    def embed(self, text: str):
        """テキストまたはテキストリストをベクトル化して返す"""
        if isinstance(text, list):
            return [self._embed_single(t) for t in text]
        else:
            return self._embed_single(text)

    def _embed_single(self, text: str):
        """1テキスト分埋め込み（キャッシュ付き）"""
        if self.use_cache and text in self._cache:
            return self._cache[text]

        vector = self.model.encode([text], normalize_embeddings=True)[0].tolist()

        if self.use_cache:
            self._cache[text] = vector

        return vector

# レジストリ登録
ModuleRegistry.register("hf_embedder", HuggingFaceEmbedder)
