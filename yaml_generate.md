## 📄 プロンプト本文（改訂版）

---

> あなたはプロフェッショナルなソフトウェアアーキテクトであり、ドキュメンテーション自動生成の専門家です。  
> 以下に提示するPythonモジュールコードを読み取り、指定された仕様に厳密に従って、そのモジュールの**メタデータ（manifest.yaml）**を生成してください。

---

> ### 🎯 出力要件
>
> 出力は**必ず厳密なYAML形式**で行い、以下のフォーマットに従ってください。
>
> ```yaml
> name: <モジュールの一意識別子（例: simple_chunker）>
> type: <モジュール種別（loader / parser / normalizer / chunker / embedder / retriever / filter / reranker / prompt_template / postprocessor / model）>
> description: <そのモジュールが何をするか、簡潔かつ実用的な日本語説明>
> inputs:
>   - name: <入力項目の名前>
>     type: <型（例: str, List[str], dictなど）>
> outputs:
>   - name: <出力項目の名前>
>     type: <型（例: str, List[str], dictなど）>
> dependencies: [<外部ライブラリ名のリスト。なければ空リスト []>]
> author: "Auto-Generated"
> license: "MIT"
> version: "1.0.0"
> ```

---

> ### 🛠 特記事項
>
> - **inputs/outputs** は、実装されているメソッド（例: `load` / `parse` / `normalize` / `chunk` / `embed` / `retrieve` / `filter` / `rerank` / `format_prompt` / `postprocess` / `generate`など）から正確に推測してください。
> - **dependencies** は、コード内のimport文から判断し、外部ライブラリのみリストアップしてください。（標準ライブラリは除外）
> - **description** は、誰が読んでも直感的に理解できる、簡潔かつ実用的な日本語で記述してください。
> - 入出力の型や内容に不明点がある場合は、仕様意図に沿って合理的に補完してください。
> - 不要な説明やコメント、出力サンプルは付けず、**manifest.yamlそのもの**のみを純粋に出力してください。

---

> ### 📥 入力データ
>
> 以下に対象モジュールのコード全文を提示します。
>
> ````python
> {ここに取得したコード全文をそのまま貼り付ける}
> ````

---