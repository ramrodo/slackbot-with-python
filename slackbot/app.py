import os
import random
from flask import Flask, request, make_response
from slack import WebClient
from slackeventsapi import SlackEventAdapter

app = Flask(__name__)

SLACKBOT_TOKEN = os.environ['SLACKBOT_TOKEN']
SLACK_EVENTS_TOKEN = os.environ['SLACK_EVENTS_TOKEN']

slack_web_client = WebClient(SLACKBOT_TOKEN)
slack_events_adapter = SlackEventAdapter(
    SLACK_EVENTS_TOKEN, "/slack/events", app)

MESSAGE_BLOCK = {
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "",
    },
}

@app.route("/slack_verification", methods=('GET', 'POST'))
def slack_verification():
    slack_event = request.get_json()

    if "challenge" in slack_event:
        return make_response(
            slack_event["challenge"],
            200,
            { "content_type": "application/json"}
        )

@slack_events_adapter.on("message")
# @app.route("/message", methods=['POST'])
# def message():
def message(payload):
    # payload = request.get_json()
    event = payload.get("event", {})
    text = event.get("text")

    if "flip a coin" in text.lower():
        channel_id = event.get("channel")
        rand_int = random.randint(0, 1)
        if rand_int == 0:
            results = "Heads"
        else:
            results = "Tails"

        message = f"The result is {results}"

        MESSAGE_BLOCK["text"]["text"] = message

        x = {"channel": channel_id, "blocks": [MESSAGE_BLOCK]}

        slack_web_client.chat_postMessage(**x)

        return x

if __name__ == "__main__":
    app.run(port=3000)

# slack_events_adapter.start(port=3000)

