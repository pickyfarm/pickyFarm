import requests

# import config
from config import settings
from . import auth


def sendMany(data):
    return requests.post(
        settings.getUrl("/messages/v4/send-many"),
        headers=auth.get_headers(settings.apiKey, settings.apiSecret),
        json=data,
    )


def sendOne(data):
    return requests.post(
        settings.getUrl("/messages/v4/send"),
        headers=auth.get_headers(settings.apiKey, settings.apiSecret),
        json=data,
    )


def post(path, data):
    return requests.post(
        settings.getUrl(path),
        headers=auth.get_headers(settings.apiKey, settings.apiSecret),
        json=data,
    )


def put(path, data, headers={}):
    headers.update(auth.get_headers(settings.apiKey, settings.apiSecret))
    return requests.put(settings.getUrl(path), headers=headers, json=data)


def get(path, headers={}):
    headers.update(auth.get_headers(settings.apiKey, settings.apiSecret))
    return requests.get(settings.getUrl(path), headers=headers)


def delete(path):
    return requests.delete(
        settings.getUrl(path), headers=auth.get_headers(settings.apiKey, settings.apiSecret)
    )
