import os
import sys
import logging
import openai
from pathlib import Path

def main():
    ENDPOINT_URL = os.environ.get("ENDPOINT_URL")
    API_KEY      = os.environ.get("API_KEY")

    path   = sys.argv[1]
    before = Path(sys.argv[2]).read_text()
    after  = Path(sys.argv[3]).read_text()

    try:
        openai.api_type    = "azure"
        openai.api_version = "2023-05-15"
        openai.api_base    = ENDPOINT_URL
        openai.api_key     = API_KEY

        aiRole = '''
あなたはコードレビューを行うAIアシスタントです。

入力は次の形式で与えられます。
- 1行目にファイルのパスが与えられます。
- "# 入力1"の後に続くコードブロックに変更前のコードが与えられます。
- "# 入力2"の後に続くコードブロックに変更後のコードが与えられます。

入力1と入力2の変更点を調べ、要約してください。
その際、次のフォーマットに従いMarkdown形式で出力してください。
## AIコードレビュー
`ファイルのパスを記載してください。`
### 変更点
変更箇所がどのように改善されたかを記載してください。
### 改善案
変更箇所をさらに改良する案を記載してください。
'''

        aiPrompt = f'''
{path}
# 入力1  
```  
{before}
```  
&nbsp;  
# 入力2  
```  
{after}
```
'''

        response = openai.ChatCompletion.create(
            deployment_id="github-app-test",
            messages=[
                {"role": "system", "content": aiRole},
                {"role": "user", "content": aiPrompt}
            ]
        )

        print(response.choices[0]["message"]["content"].strip())

    except Exception as e:
        logging.error(e)

if __name__ == "__main__":
        main()