## github-app-on-azure

### 概要

この Actions はプルリクエスト内の追加・変更されたファイルに対し、ChatGPT を用いてコードレビューを行います。

### 環境構築

1. リポジトリのシークレットに以下のキーを登録する

| Key          | Value                  |
| ------------ | ---------------------- |
| ENDPOINT_URL | API の URL             |
| API_KEY      | API のシークレットキー |

2. `.github/.whitelist`にコードレビューの対象となるファイル拡張子を入力する

```
.py
.java
.php
```

### 注意事項

- `.github/.whitelist`には拡張子以外の文字を入力しないでください。
- 使用する API は AzureOpenAI を使用してください。
