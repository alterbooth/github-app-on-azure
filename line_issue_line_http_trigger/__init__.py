from linebot import LineBotApi
from linebot.models import TextSendMessage
from github import Github, GithubIntegration

import azure.functions as func
import os
import base64

lineChannel = LineBotApi(os.environ["LINE_BOT_CHANNEL_TOKEN"])

git_integration = GithubIntegration(
    os.environ["APP_ID"],
    base64.b64decode(os.environ["PRIVATE_KEY"].encode()).decode()
)

def main(req: func.HttpRequest) -> func.HttpResponse:
    payload = req.get_json()

    if payload["events"][0]["message"]["text"] is not None:
        message = payload["events"][0]["message"]["text"].split("\r\n")
        if message[0] == "Issueに返信":
            repositoryId = message[1].split("/")
            owner = repositoryId[0]
            repositoryName = repositoryId[1]
            issueId = repositoryId[2]
            try:
                git_connection = Github(
                    login_or_token=git_integration.get_access_token(
                        git_integration.get_repo_installation(owner, repositoryName).id
                    ).token
                )
                repository = git_connection.get_repo(f"{owner}/{repositoryName}")
                issue = repository.get_issue(int(issueId))

                commentLines = []
                for i in range(3, len(message)):
                    commentLines.append(message[i])
                comment = "\r\n".join(commentLines)

                if comment == "":
                    replyMessage = "コメントが空です"
                else:
                    lineUser = lineChannel.get_profile(payload["events"][0]["source"]["userId"]).as_json_dict()["displayName"]
                    issue.create_comment("### " + lineUser + "からの返信 (Line)\r\n" + comment)
                    replyMessage = "コメントを送信しました"
            except Exception:
                replyMessage = "コメントの送信に失敗しました"
            finally:
                lineChannel.reply_message(
                    payload["events"][0]["replyToken"],
                    TextSendMessage(replyMessage)
                )

    return func.HttpResponse(status_code=200)