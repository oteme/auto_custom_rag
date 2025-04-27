## 📄 プロンプト本文

> あなたはプロフェッショナルなソフトウェアアーキテクトです。  
> 以下に提示するPythonモジュールコードを読み取り、  
> 指定された仕様に従って、そのモジュールの**メタデータ（manifest.yaml）**を生成してください。
> 
> 出力形式は必ず**YAML**形式で、以下のフォーマットに厳密に従ってください。
> 
> ### 出力するYAMLのフォーマット
> ```yaml
> name: <モジュールの一意識別子（例: simple_chunker）>
> type: <モジュール種別（loader / parser / normalizer / chunker / embedder / retriever / filter / reranker / prompt_template / postprocessor / model）>
> description: <そのモジュールが何をするか、簡潔で実用的な日本語説明>
> inputs:
>   - <入力名>: <型（str, List[str], dict,など）>
> outputs:
>   - <出力名>: <型（str, List[str], dict,など）>
> dependencies: [<必要な外部ライブラリ（あれば。なければ空リスト>)]
> author: "Auto-Generated"
> license: "MIT"
> version: "1.0.0"
> ```
> 
> ### 特記事項
> - **inputs/outputs** は、実装されているメソッド（主に`load`/`parse`/`normalize`/`chunk`/`embed`/`retrieve`/`filter`/`rerank`/`format_prompt`/`postprocess`/`generate`）から推測してください。
> - **dependencies** は、import文から自動的に判断してください。（例: numpy, fitz, transformersなど）
> - **description** は、誰が読んでもモジュールの役割がすぐわかる実用的な説明にしてください。
> - もし情報が不足している場合は、推測に基づいて適切に補完してください。
> 
> 
> ### 入力データ
> 以下が対象モジュールのコード全文です。
> ````python
> {ここにuithubで取得したコードをそのまま貼り付ける}
> ````

---

# ✨ このプロンプトでできること

- **uithubで取得したコード全文をコピペするだけ**  
- **各モジュールごとに完璧なmanifest.yamlを自動生成**  
- **人間の手直し最小限**（99%はそのまま使えるレベル）  

---

# ✅ ワークフローまとめ

1. **uithub**で対象モジュールのテキストデータを取得する  
2. 上記のプロンプトに **コード全文をそのまま貼り付ける**  
3. **生成AI（ChatGPTやClaude）に食わせる**  
4. 出力された **YAMLをそのまま保存**（modules/xxx/manifest.yaml）

