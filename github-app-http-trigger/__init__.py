import logging
import os
import base64
import azure.functions as func
from github import Github, GithubIntegration
import openai
import urllib.parse
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        #GithubAppsの環境変数読み込み
        app_id = os.environ.get("APP_ID")
        private_key = os.environ.get("PrivateKey")
        #OpenAIの設定
        openai.api_type = "azure"
        openai.api_base = os.environ.get("OPEN_AI_URL")
        openai.api_version = "2023-03-15-preview"
        openai.api_key = os.environ.get("OPEN_AI_KEY")

        logging.info(private_key)
        private_key = base64.b64decode(private_key).decode()
        logging.info(private_key)
    except Exception as e:
        logging.error(e)
        print(e)
        return func.HttpResponse(500, "private key is invalid")

    # Create an GitHub integration instance
    integration = GithubIntegration(
        app_id,
        private_key,
    )
    payload = req.get_json()
    logging.info(payload)
    keys = payload.keys()

    if payload['action'] == 'opened':
        if "issue" in keys:
            try:
                installation_id = payload['installation']['id']
                repo_full_name = payload['repository']['full_name']
                issue_number = payload['issue']['number']
                user = payload['issue']['user']['login']

                access_token = integration.get_access_token(installation_id).token
                github = Github(access_token)

                repo = github.get_repo(repo_full_name)
                issue = repo.get_issue(issue_number)

                issue.create_comment('Hello, @{}!'.format(user))

                return func.HttpResponse("OK", status_code=200)
            except Exception as e:
                logging.error(e)
                return func.HttpResponse("Something is wrong with the payload of the issue.", status_code=400)
        elif "pull_request" in keys:
            try:
                installation_id = payload['installation']['id']
                repo_full_name = payload['repository']['full_name']
                pull_request_number = payload['pull_request']['number']
                user = payload['pull_request']['user']['login']

                access_token = integration.get_access_token(installation_id).token
                github = Github(access_token)

                repo = github.get_repo(repo_full_name)
                pull_request = repo.get_pull(pull_request_number)
                text = requests.get(payload["pull_request"]["diff_url"])
                response = openai.ChatCompletion.create(
                    engine="github-app-test",
                    messages=[{"role": "system", "content": "You are an AI assistant that helps people find information."}, {"role": "user", "content": f"今から示すのはgithubにおける差分のファイルです。あなたをこれを見てどの部分に変更が加わったかを端的に説明してください。また誤りやタイピングのミス等を発見した場合はそれも報告してください。また、質問への返答はですます調で答えてください。      \n  \n  \n{text.text}"}, ],
                    temperature=0.7,
                    max_tokens=800,
                    top_p=0.95,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None
                )

                decoded_text = urllib.parse.unquote(response["choices"][0]["message"]["content"])
                pull_request.create_issue_comment(
                    decoded_text
                )
                return func.HttpResponse("OK", status_code=200)
            except Exception as e:
                logging.error(e)
                return func.HttpResponse("Something is wrong with the payload of the pull_request.", status_code=400)
        
        return func.HttpResponse("this payload did not include pull_request or issue", status_code=400)
    return func.HttpResponse("this payload action was not matched.", status_code=400)
