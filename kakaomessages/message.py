import requests
import sys

# import config
from config import settings
from .auth import *


def sendMany(data):
    return requests.post(
        settings.getUrl("/messages/v4/send-many"),
        headers=get_headers(settings.apiKey, settings.apiSecret),
        json=data,
    )


def sendOne(data):
    return requests.post(
        settings.getUrl("/messages/v4/send"),
        headers=get_headers(settings.apiKey, settings.apiSecret),
        json=data,
    )


def post(path, data):
    return requests.post(
        settings.getUrl(path),
        headers=get_headers(settings.apiKey, settings.apiSecret),
        json=data,
    )


def put(path, data, headers={}):
    headers.update(get_headers(settings.apiKey, settings.apiSecret))
    return requests.put(settings.getUrl(path), headers=headers, json=data)


def get(path, headers={}):
    headers.update(get_headers(settings.apiKey, settings.apiSecret))
    return requests.get(settings.getUrl(path), headers=headers)


def delete(path):
    return requests.delete(
        settings.getUrl(path), headers=get_headers(settings.apiKey, settings.apiSecret)
    )
