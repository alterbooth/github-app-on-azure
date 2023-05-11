import logging
import os
import azure.functions as func
from github import Github, GithubIntegration

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    app_id = '321478'
    # Read the bot certificate
    # with open("github-app-http-trigger/private-key.pem") as cert_file:
    #     app_key = cert_file.read()
    #     logging.info(app_key)
    try:
        private_key = os.environ.get("PrivateKey")
        logging.info(private_key)
        private_key = private_key.replace("\\n", "\n")
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
            installation_id = payload['installation']['id']
            repo_full_name = payload['repository']['full_name']
            issue_number = payload['issue']['number']
            user = payload['issue']['user']['login']

            access_token = integration.get_access_token(installation_id).token
            github = Github(access_token)

            repo = github.get_repo(repo_full_name)
            issue = repo.get_issue(issue_number)

            issue.create_comment('Hello, @{}!'.format(user))
        elif "pull_request" in keys:
            installation_id = payload['installation']['id']
            repo_full_name = payload['repository']['full_name']
            pull_request_number = payload['pull_request']['number']
            user = payload['pull_request']['user']['login']

            access_token = integration.get_access_token(installation_id).token
            github = Github(access_token)

            repo = github.get_repo(repo_full_name)
            pull_request = repo.get_pull(pull_request_number)
            pull_request.create_comment('Hello, @{}!'.format(user))

    return func.HttpResponse("OK", status_code=200)
