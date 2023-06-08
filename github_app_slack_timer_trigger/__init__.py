import json
import requests
import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    if mytimer.past_due:
        print('The timer is past due!')
    url = 'https://hooks.slack.com/services/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'
    payload = {
        "text": "日報書いてね！！",
        "username": "Azure Functions Bot",
        "icon_emoji": ":zap:",
        "channel": "#webhook"
    }
    response=requests.post(url, data=json.dumps(payload))
    print(response)
    print("Success??")
    # print("Timer last triggered at " + str(mytimer.last))
    # print("Timer triggered at " + str(mytimer.next))
    if __name__ == '__main__':
        main()
