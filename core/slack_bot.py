from slack_sdk import WebhookClient
from slack_sdk.errors import SlackApiError

import os
import ssl, certifi


def send_message_to_slack(channel, message):

    ssl_context = ssl.create_default_context(cafile=certifi.where())

    client = WebhookClient(url=os.environ.get('SLACK_WEBHOOK_URL'), ssl=ssl_context)

    try:
        res = client.send(blocks=message)
        

    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")
