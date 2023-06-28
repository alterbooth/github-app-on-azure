## github-app-on-azure
### 概要
このActionsはプルリクエスト内の追加・変更されたファイルに対し、ChatGPTを用いてコードレビューを行います。

### 環境構築
1. リポジトリのシークレットに以下のキーを登録する

| Key | Value |
| - | - |
| ENDPOINT_URL | APIのURL |
| API_KEY | APIのシークレットキー |

2. `.github/.whitelist`にコードレビューの対象となるファイル拡張子を入力する
```
.py
.java
.php
```

### 注意事項
- `.github/.whitelist`には拡張子以外の文字を入力しないでください。
- 使用するAPIはAzureOpenAIを使用してください。