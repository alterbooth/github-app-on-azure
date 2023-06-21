import os
import sys
import logging
import openai
from pathlib import Path

def main():
    #ENDPOINT_URL = os.environ.get("ENDPOINT_URL")
    #API_KEY      = os.environ.get("API_KEY")
    #ENDPOINT_URL = os.environ.get("https://github-app-test.openai.azure.com/")
    #API_KEY      = os.environ.get("28dc9afeb20f45c68737b892c1db04c8")

    try:
        openai.api_type    = "azure"
        openai.api_version = "2023-05-15"
        openai.api_base    = "https://github-app-test.openai.azure.com/"
        openai.api_key     = "28dc9afeb20f45c68737b892c1db04c8"

        response = openai.ChatCompletion.create(
            deployment_id="github-app-test",
            messages=[
                {"role": "system", "content": "You are an AI assistant that helps people find information."},
                {"role": "user", "content": "日本の国歌の歌詞を教えてください"}
            ]
        )
        print(response.choices[0].message)

    except Exception as e:
        logging.error(e)

if __name__ == "__main__":
        main()