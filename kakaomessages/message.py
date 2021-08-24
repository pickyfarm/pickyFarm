import requests
import sys

# import config
from config.settings import base
from .auth import *


def sendMany(data):
    return requests.post(
        base.getUrl("/messages/v4/send-many"),
        headers=get_headers(base.apiKey, base.apiSecret),
        json=data,
    )


def sendOne(data):
    return requests.post(
        base.getUrl("/messages/v4/send"),
        headers=get_headers(base.apiKey, base.apiSecret),
        json=data,
    )


def post(path, data):
    return requests.post(
        base.getUrl(path),
        headers=get_headers(base.apiKey, base.apiSecret),
        json=data,
    )


def put(path, data, headers={}):
    headers.update(get_headers(base.apiKey, base.apiSecret))
    return requests.put(base.getUrl(path), headers=headers, json=data)


def get(path, headers={}):
    headers.update(get_headers(base.apiKey, base.apiSecret))
    return requests.get(base.getUrl(path), headers=headers)


def delete(path):
    return requests.delete(base.getUrl(path), headers=get_headers(base.apiKey, base.apiSecret))
