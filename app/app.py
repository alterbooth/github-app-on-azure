import os
import requests

from flask import Flask, request
from github import Github, GithubIntegration


app = Flask(__name__)
# MAKE SURE TO CHANGE TO YOUR APP NUMBER!!!!!
app_id = '321478'
# Read the bot certificate
with open("./private-key.pem") as cert_file:
    app_key = cert_file.read()

# Create an GitHub integration instance
integration = GithubIntegration(
    app_id,
    app_key,
)

@app.route("/")
def index():
    return "Hello, world!"


@app.route("/webhook", methods=['POST'])
def bot():
    payload = request.get_json()
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
        
    return "ok"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
