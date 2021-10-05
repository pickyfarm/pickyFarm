from urllib import parse
import cryptocode
import os

from cryptocode.myfunctions import decrypt

def decode_url_string(url_str):
    percent_dec = parse.unquote(url_str)
    cryptcode_dec = cryptocode.decrypt(percent_dec, os.environ.get("SECRET_KEY"))
    return cryptcode_dec


def encode_string_to_url(str):
    cryptcode_enc = cryptocode.encrypt(str, os.environ.get("SECRET_KEY"))
    percent_enc = parse.quote(cryptcode_enc)
    return percent_enc