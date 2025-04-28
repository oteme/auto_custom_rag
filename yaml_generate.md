

##  manifest.yaml 生成プロンプト（params 対応版）


## 📄 モジュール manifest 生成プロンプト

> あなたはプロフェッショナルなソフトウェアアーキテクトであり、ドキュメント自動生成の専門家です。  
> 以下の Python モジュールコードを読み取り、**manifest.yaml** を出力してください。

### 🎯 出力要件
- 出力は**厳密な YAML** で、次のキーを必ず含めること
```yaml
name: <モジュールの一意識別子>
type: <loader|parser|normalizer|chunker|embedder|retriever|filter|reranker|prompt_template|postprocessor|model|session_manager|mode>
description: <詳細で実用的な日本語説明>
inputs:
  - name: <入力名>
    type: <型>
outputs:
  - name: <出力名>
    type: <型>
params:
  - name: <パラメータ名>
    type: <型>
    default: <デフォルト値またはnull>
dependencies: [<外部ライブラリ名のリスト ※標準ライブラリ除く>]
author: "Auto-Generated"
license: "MIT"
version: "1.0.0"
```
### 🛠 指示
- **inputs / outputs** は主な公開メソッドから推測してください。
- **params** は `__init__(self, …)` の引数を列挙し、デフォルトが無ければ `null`。
- import 文から外部ライブラリのみ dependencies に列挙してください。
- 不明点があれば合理的に補完し、**manifest.yaml 本体のみ** を出力してください。

### 📥 入力データ
```python
{ここに対象モジュールのコード全文をそのまま貼り付ける}
```
