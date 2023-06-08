import json
import os
import logging
import urllib.request
import azure.functions as func
from github import Github, GithubIntegration
import requests

logging.info('Python HTTP trigger function processed a request.')

#GithubAppsの環境変数読み込み
app_id = os.environ.get("APP_ID")
private_key = os.environ.get("PRIVATE_KEY")

with open("c:/toshi-github-on-azure-private-key.pem") as key:
    private_key = key.read()

integration = GithubIntegration(
    app_id,
    private_key,
)

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # logging.info(req)
    # logging.info(req.get_json())
    payload = req.get_json()
    # logging.info(payload)
    keys = payload.keys()

    if payload['action'] == 'opened':
        if "issue" in keys:
            installation_id = payload['installation']['id']
            repo_full_name = payload['repository']['full_name']
            issue_number = payload['issue']['number']
            user = payload['issue']['user']['login']
            issue_url = payload['issue']['html_url']

            # access_token = integration.get_access_token(installation_id).token
            # github = Github(access_token)

            # repo = github.get_repo(repo_full_name)
            # issue = repo.get_issue(issue_number)

            # issue.create_comment('@{}がissueを開きました!'.format(user))

            headers = {"Content-type": "application/json"}
            data = {
                "text": "@{}が{}でissueを開きました\n{}".format(user,repo_full_name,issue_url),
                "username": "App Function Bot",
                "emoji_icon": ":zap:",
                "channel":"webhook"
            }
            response = requests.post(
                "https://hooks.slack.com/services/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",
                headers=headers,
                data=json.dumps(data)
            )
    return func.HttpResponse(status_code=200)


    