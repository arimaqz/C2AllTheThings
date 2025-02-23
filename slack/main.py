import slack
from flask import Flask
from slackeventsapi import SlackEventAdapter
import subprocess

SLACK_TOKEN="REDACTED"
SIGNING_SECRET = "REDACTED"

def Exec(cmd):
    output = subprocess.check_output(cmd, shell=False)
    return output

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)

client = slack.WebClient(token=SLACK_TOKEN)

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    text = event.get('text')
    output = Exec(text).decode()
    client.chat_postMessage(channel=channel_id,text=output)

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
