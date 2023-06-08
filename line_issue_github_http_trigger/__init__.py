from linebot import LineBotApi
from linebot.models import FlexSendMessage

import azure.functions as func
import re
import urllib.parse
import os

lineChannel = LineBotApi(os.environ["LINE_BOT_CHANNEL_TOKEN"])
lineBotId = urllib.parse.quote(os.environ["LINE_BOT_ID"])

def main(req: func.HttpRequest) -> func.HttpResponse:
    payload = req.get_json()
    keys = payload.keys()

    if "comment" in keys:
        
        if payload["comment"]["user"]["type"] == "Bot":
            return func.HttpResponse(status_code=200)

        lineChannel.broadcast(
            FlexSendMessage(
                alt_text="Issue #" + str(payload["issue"]["number"]) + "に返信がありました",
                contents=getFlexMessage(
                    payload["issue"]["title"],
                    payload["comment"]["body"],
                    payload["issue"]["number"],
                    payload["repository"]["full_name"] + "/" + str(payload["issue"]["number"]),
                    payload["comment"]["user"]["login"],
                    payload["comment"]["html_url"]

                )
            )
        )

    else:
        lineChannel.broadcast(
            FlexSendMessage(
                alt_text="新規Issueが立ちました #" + str(payload["issue"]["number"]),
                contents=getFlexMessage(
                    payload["issue"]["title"],
                    payload["issue"]["body"] if payload["issue"]["body"] != None else "コメントはありません",
                    payload["issue"]["number"],
                    payload["repository"]["full_name"] + "/" + str(payload["issue"]["number"]),
                    payload["issue"]["user"]["login"],
                    payload["issue"]["html_url"]
                )
            )
        )
    
    return func.HttpResponse(status_code=200)

# FlexMessage用テンプレート
def getFlexMessage(issueTitle, issueComment, issueId, repositoryId, commentBy, issueUrl):
    comment = []
    comments = issueComment.splitlines()
    for line in comments:
        text = {}
        if re.match("#+", line):
            text["weight"] = "bold"
        line = re.sub("#+ ", "", line)
        line = re.sub("- ", "・", line)
        text["type"] = "text"
        if line == "":
            text["text"] = " "
        else:
            text["text"] = line
        comment.append(text)

    json = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": issueTitle,
                            "size": "lg",
                            "weight": "bold",
                            "flex": 8
                        },
                        {
                            "type": "text",
                            "text": "#" + str(issueId),
                            "size": "lg",
                            "flex": 0
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": "@" + commentBy
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": comment,
                    "margin": "xl"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": "Issueを見る",
                        "uri": issueUrl
                    }
                },
                {
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": "返信する",
                        "uri": "https://line.me/R/oaMessage/" + lineBotId + "/" + "Issue%E3%81%AB%E8%BF%94%E4%BF%A1%0D%0A" + urllib.parse.quote(repositoryId) + "%0D%0A--%E4%BB%A5%E4%B8%8B%E3%81%AB%E3%82%B3%E3%83%A1%E3%83%B3%E3%83%88--%0D%0A"
                    }
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "baseline",
            "contents": [
                {
                    "type": "text",
                    "text": repositoryId
                }
            ]
        },
        "styles": {
            "body": {
                "separator": False
            }
        }
    }
    return json