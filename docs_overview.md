
# ① 「auto-custom-rag」プロジェクト 説明文書（完全最新版）


# ✨ auto-custom-rag ─ 完全版ドキュメント
（2025-04 更新）

## 1. 🛠 プロジェクト概要
**auto-custom-rag** は  
**モジュール着せ替え × コンフィグ駆動 × 未来的自律化** をコンセプトにした  
Retrieval Augmented Generation（RAG）パイプラインエンジンです。  
YAML／Python辞書の **config を書き換えるだけ** で、  
*データ取込 → 検索 → プロンプト生成 → モデル推論 → 後処理* の各段階を  
自由に組み替えて運用できます。

---

## 2. 🎯 設計思想
| 観点 | 具体 |
| --- | --- |
| モジュール完全独立 | Loader / Parser … Model まで 12 カテゴリを完全分離 |
| Registry + 動的 import | `registry.py` がパスを推測し自動 import・登録 |
| 設定ファイル完結 | コードを触らず **config だけ** で着せ替え |
| manifest 必須 | 各モジュールは `manifest.yaml` で I/O・依存を宣言 |
| params 統一 | すべての `__init__(**params)` で外部設定を注入 |
| flow 駆動 | `config["flow"]` 順に Manager が実行するだけ |
| runtime_pipeline | SessionManager / Model / Mode を 1 束で管理 |
| retrieval_steps | `retrieval_pipeline.steps` で検索フローを完全宣言 |
| 将来像 | 生成AIが最適 config を自己生成 → **自律パイプライン** |

---

## 3. 🏗 全体アーキテクチャ
```
┌───────────┐     ┌──────────────┐     ┌────────────────┐
│ Data Layer│ →  │ RetrievalFlow │ →  │ GenerationFlow │
└───────────┘     └──────────────┘     └────────────────┘
      │                   │                     │
      ▼                   ▼                     ▼
 Loader→Parser→…  Retriever→Filter→Reranker  Prompt→Model→PostProc
```
*各矢印は **config に列挙したモジュール** が順に呼ばれるだけ。*

---

## 4. 🔄 主要フロー

### 4-1 initialize_pipeline()
1. config 読取 → モジュールを動的 import
2. manifest.yaml を読んで I/O 互換チェック
3. Retrieval は `steps` を走査して retriever / filter / reranker を初期化

### 4-2 run()
`config["flow"]` に並んだパイプライン名を順次実行  
（例）`["data_pipeline","generation_pipeline","runtime_pipeline"]`

### 4-3 manager.retrieve_chunks(query)
`retrieval_pipeline.steps` に従って柔軟に  
retriever → filters → reranker を実行しチャンクを返却。

---

## 5. 🔥 現在実装済みモジュール（抜粋）
| 種別 | 名称 | 役割 |
| --- | --- | --- |
| loader | **pdf_loader** | ローカル PDF 取込 |
| retriever | **faiss_retriever** | FAISS 高速検索・永続化対応 |
| model | **openai_model / together_model / anthropic_model / local_hf_model** | API / ローカル両対応。api_key は params or .env |

---

## 6. 📐 config スキーマ（抜粋）

```yaml
data_pipeline:
  loaders:
    - name: pdf_loader
      params: {path: data/pdfs}
  parser: {name: simple_parser, params: {}}
  …

retrieval_pipeline:
  steps:
    - {type: retriever, name: simple_retriever, params: {}}
    - {type: filter,    name: simple_filter,    params: {}}
    - {type: reranker,  name: simple_reranker,  params: {}}

generation_pipeline:
  prompt_template: {name: simple_prompt_template, params: {}}
  postprocessors:
    - {name: simple_postprocessor, params: {}}

runtime_pipeline:
  session_manager: {name: simple_session_manager, params: {}}
  model:           {name: openai_model, params: {temperature: 0.7}}
  mode:            {name: chat_mode,   params: {}}

flow: ["data_pipeline", "generation_pipeline", "runtime_pipeline"]
```

---

## 7. 🚀 今後のロードマップ （要約）
- Cache 層追加／Streaming 対応
- manifest 完全整合チェックツール
- 生成AIによる自動 config 最適化
- マルチモーダル拡張　…etc

---

## 8. 📄 ライセンス
MIT License / コントリビューション大歓迎！  
新モジュール PR 時は **manifest.yaml とテスト** を添付してください。

---

## 9. ✨ 一言
**auto-custom-rag** は「設定を書くだけ」で  
“あなた専用 RAG” を即座に組める未来志向エンジンです。  
OSS として一緒に育てていきましょう！ 🚀

### 📝 今後のやることリスト（詳細版・カテゴリ別）

---

#### 1. **Data Ingestion 層**
| 優先度 | タスク | 補足 |
|:--:|:--|:--|
| ★★★ | **メタ付き Chunk 化** | チャンクにページ番号・原文位置・ファイル名などを付与し、検索結果にメタを返す |
| ★★☆ | **WebLoader 実装** | URL / サイトマップ / RSS などをクロールして取り込み |
| ★☆☆ | **CSV・Markdown Loader** | テーブル系・プレーン MD をパーサー込みで読み込む |

---

#### 2. **Retrieval Pipeline**
| 優先度 | タスク | 補足 |
| --- | --- | --- |
| ★★★ | **スコア合成対応** | キーワード BM25 + ベクトル類似度を重み付け合算（config で比率指定） |
| ★★★ | **メタ情報検索** | タグ・著者・日付といった属性条件フィルタを追加 |
| ★★☆ | **FAISS インデックス永続化 UI** | `save_index()` / `load_index()` を CLI か API で呼べるように |
| ★☆☆ | **Query Expansion Filter** | 同義語展開・Embedding 近傍語でクエリを拡張 |

---

#### 3. **Generation Pipeline**
| 優先度 | タスク | 補足 |
| --- | --- | --- |
| ★★★ | **ストリーミング出力** | `model.generate()` を generator 化し、Mode で逐次表示 |
| ★★★ | **Cache 層** | Prompt+Hash → Response を Redis / SQLite に保存・再利用 |
| ★★☆ | **高度 PromptTemplate** | ロール別セクション・Chain of Thought・ツール呼び出しプレースホルダー |
| ★☆☆ | **PostProcessor Chain** | 正規表現置換・要約・翻訳など複数後処理をチェーン実行できる仕組み |

---

#### 4. **Model 層**
| 優先度 | タスク | 補足 |
| --- | --- | --- |
| ★★★ | **リトライ＆レート制御** | API 上限・ネットワーク例外時の自動リトライ、指数バックオフ |
| ★★☆ | **マルチモデル Router** | cost / latency / 機密度に応じてモデル切替（例：短文は GPT-3.5、長文は Llama） |
| ★★☆ | **エンベディング API 統合** | text-embedding-3, Cohere Embed などを params で選択 |
| ★☆☆ | **量子化ローカルモデル** | GGUF / GPTQ 自動ロード、CPU でも動くサンプル |

---

#### 5. **Runtime / Mode**
| 優先度 | タスク | 補足 |
| --- | --- | --- |
| ★★★ | **Tool-Calling Mode** | 関数呼び出し or JSON mode に対応し、ツール実行→再呼び出しループ |
| ★★☆ | **Summarize Mode** | 大量文書を一括要約し、段階的に縮約 |
| ★☆☆ | **Voice Chat Mode** | 音声認識 + TTS で音声入出力 |

---

#### 6. **共通インフラ**
| 優先度 | タスク | 補足 |
| --- | --- | --- |
| ★★★ | **manifest 互換チェッカー** | CI で I/O 型・依存ライブラリを静的検証 |
| ★★☆ | **自動 config 最適化エージェント** | 生成AIがタスク説明→最適モジュール＋params＋flow を提案 |
| ★★☆ | **CLI & REST API** | `acr run --config xxx.yaml` や `/v1/query` エンドポイント |
| ★☆☆ | **Docker/Compose テンプレ** | GPU / CPU 両対応のコンテナ一発起動 |

---

#### 7. **ドキュメント & OSS 運用**
| 優先度 | タスク | 補足 |
| --- | --- | --- |
| ★★★ | **Usage Cookbook** | 代表ユースケース別の config サンプル集 |
| ★★☆ | **Contribution Guide** | モジュール追加手順・テスト・PR テンプレ |
| ★★☆ | **単体 / 結合テスト整備** | pytest + fixture で主要モジュールのゴールデンテスト |
| ★☆☆ | **Benchmarks** | retrieval latency / token cost / response BLEU 等の計測スクリプト |

---

> **★の数 = 重要度 / 早急性（3 が最優先）**  

このリストをベースに、優先度高いものから順に実装・レビューを進めれば OK です！