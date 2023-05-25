from azure.functions import HttpRequest
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from github_app_http_trigger import main

def test_main_opened_issue():
    request = HttpRequest(
        method='POST',
        url='',
        body=b'{"action": "opened", "installation": {"id": 36641754}, "repository": {"full_name": "yamato0211/goChan"}, "issue": {"number": 1, "user": {"login": "yamato0211"}}}',
        headers={
            'Content-Type': 'application/json'
        }
    )
    response = main(request)
    assert response.status_code == 200
    assert response.get_body() == b'OK'


def test_main_opened_pull_request():
    request = HttpRequest(
        method='POST',
        url='',
        body=b'{"action": "opened", "installation": {"id": 36641754}, "repository": {"full_name": "yamato0211/goChan"}, "pull_request": {"number": 2, "diff_url": "https://github.com/yamato0211/goChan/pull/2.diff", "user": {"login": "yamato0211"}}}',
        headers={
            'Content-Type': 'application/json'
        }
    )
    response = main(request)
    assert response.status_code == 200
    assert response.get_body() == b'OK'


def test_main_invalid_action():
    request = HttpRequest(
        method='POST',
        url='',
        body=b'{"action": "invalid", "installation": {"id": 36641754}, "repository": {"full_name": "yamato0211/goChan"}, "issue": {"number": 1, "user": {"login": "yamato0211"}}}',
        headers={
            'Content-Type': 'application/json'
        }
    )
    response = main(request)
    assert response.status_code == 400
    assert response.get_body() == b'this payload action was not matched.'

def test_main_invalid_event():
    request = HttpRequest(
        method='POST',
        url='',
        body=b'{"action": "opened", "installation": {"id": 36641754}, "repository": {"full_name": "yamato0211/goChan"}, "invalid": {"number": 1, "user": {"login": "yamato0211"}}}',
        headers={
            'Content-Type': 'application/json'
        }
    )
    response = main(request)
    assert response.status_code == 400
    assert response.get_body() == b'this payload did not include pull_request or issue.'

def test_main_wrong_issue_payload():
    request = HttpRequest(
        method='POST',
        url='',
        body=b'{"action": "opened", "installation": {"id": 36641754}, "repository": {"full_name": "yamato0211/goChan"}, "issue": {"number": "invalid", "user": {"login": "yamato0211"}}}',
        headers={
            'Content-Type': 'application/json'
        }
    )
    response = main(request)
    assert response.status_code == 400
    assert response.get_body() == b'Something is wrong with the payload of the issue.'


def test_main_wrong_pull_request_payload():
    request = HttpRequest(
        method='POST',
        url='',
        body=b'{"action": "opened", "installation": {"id": 36641754}, "repository": {"full_name": "yamato0211/goChan"}, "pull_request": {"number": "invalid", "diff_url": "https://github.com/yamato0211/goChan/pull/2.diff", "user": {"login": "yamato0211"}}}',
        headers={
            'Content-Type': 'application/json'
        }
    )
    response = main(request)
    assert response.status_code == 400
    assert response.get_body() == b'Something is wrong with the payload of the pull_request.'
