import json
import logging
import urllib.request
import azure.functions as func
from github import Github, GithubIntegration
import requests

# print('Python HTTP trigger function processed a request.')
# app_id = 337955

# with open("c:/toshi-github-on-azure-private-key.pem") as key:
#     private_key = key.read()

# integration = GithubIntegration(
#     app_id,
#     private_key,
# )

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    headers = {"Content-type": "application/json"}
    data = {
        "text": "Test",
        "username": "Test",
        "channel":"webhook"
    }
    response = requests.post(
        "https://hooks.slack.com/services/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",
        headers=headers,
        data=json.dumps(data)
    )
    # logging.info(req)
    # logging.info(req.get_json())
    # payload = req.get_json()
    # logging.info(payload)
    # keys = payload.keys()

    # if payload['action'] == 'opened':
    #     if "issue" in keys:
    #         # installation_id = payload['installation']['id']
    #         # repo_full_name = payload['repository']['full_name']
    #         # issue_number = payload['issue']['number']
    #         # user = payload['issue']['user']['login']

    #         # access_token = integration.get_access_token(installation_id).token
    #         # github = Github(access_token)

    #         # repo = github.get_repo(repo_full_name)
    #         # issue = repo.get_issue(issue_number)

    #         # issue.create_comment('@{}がissueを開きました!'.format(user))

    # url = "https://hooks.slack.com/services/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"
    # header = {"Content-type": "application/json"}
    # payload = {
    #     "text": "issueがたったよ",
    #     "username": "Azure Functions Bot",
    #     "channel": "webhook"
    # }
    # req = urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST", headers=header)
    # with urllib.request.urlopen(req) as t:
    #     print(t.read())

    #         print(response)
    #         print("Success??")
    #         # print("Timer last triggered at " + str(mytimer.last))
    #         # print("Timer triggered at " + str(mytimer.next))
    return func.HttpResponse(status_code=200)


    