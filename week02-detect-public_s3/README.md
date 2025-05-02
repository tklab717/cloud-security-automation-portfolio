# Week 0２ - S3パブリック検出スクリプト

## 概要

このスクリプトは、AWSアカウント内の全てのS3バケットをチェックし、
不特定多数のユーザからアクセス可能なバケットを検出し、その結果を管理者へ報告します。
これにより、S3に関するセキュリティリスクを早期に発見できます。

---
## 使用技術・ライブラリ

- Python 3.9.6+
- boto3 (AWS SDK for Python)
- pytest (単体テスト用)
- moto (AWSモックライブラリ)

---

## 機能

- すべてのS3バケットの取得（`list_buckets`）
- 各バケットのACL（`get_bucket_acl`）をチェックし、`AllUsers`/`AuthenticatedUsers`の存在を確認
- 各バケットのポリシーステータス（`get_bucket_policy_status`）を確認し、パブリックポリシーかを判定
- 検出結果をコンソールに出力（オプションでファイル出力も可能）

---

## 使い方

### 1. 事前準備

- AWS CLIの認証情報（`~/.aws/credentials`）を設定してください
- Python仮想環境を有効化することを推奨します

### 2. セットアップ

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

### スクリプト実行

```bash
python3 detect-public_s3.py
```

### テスト方法
```bash
pytest test_detect-public_s3.py
```
#### テスト内容


### ディレクトリ構成
```plaintext
week02-detect-public-s3/
├── detect_public_s3.py
├── test_detect_public_s3.py
├── requirements.txt
└── README.md