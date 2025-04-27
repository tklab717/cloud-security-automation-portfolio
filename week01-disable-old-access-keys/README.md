# Week 01 - IAMアクセスキー無効化スクリプト

## 概要

AWS IAMユーザーのアクセスキーを監査し、**90日以上使用されていないアクセスキーを自動で無効化する**スクリプトです。

セキュリティ強化のため、長期間使用されていないアクセスキーを無効化

---
## 使用技術・ライブラリ

- Python 3.9+
- boto3 (AWS SDK for Python)
- pytest (単体テスト用)
- moto (AWSモックライブラリ)

---

## 機能

- すべてのIAMユーザーのアクセスキーを取得
- 各キーの最終使用日を確認
- 最終使用日が90日以上前、もしくは未使用のアクセスキーを自動で無効化
- 実行結果をコンソールに出力

---

## 使い方

### 事前準備

- AWS CLIで認証情報（`~/.aws/credentials`）を設定する
- 仮想環境（venv）を推奨

### セットアップ手順

```bash
# 仮想環境を作成して有効化
python3 -m venv venv
source venv/bin/activate

# 必要なライブラリをインストール
pip install -r requirements.txt
```

### スクリプト実行

```bash
python disable_old_keys.py
```

### テスト方法
```bash
pytest test_disable_old_keys.py
```
#### テスト内容
- is_key_old関数の単体テスト
- disable_old_keys関数のテスト
  - motoによる仮想IAM環境にて動作検証

### ディレクトリ構成
```plaintext
week01-disable-old-access-keys/
├── disable_old_keys.py       # 本体スクリプト
├── test_disable_old_keys.py  # テストスクリプト
├── requirements.txt          # 必要ライブラリ
└── README.md                 # この説明ファイル
