from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

# WSGI application
WSGI_APPLICATION = "config.wsgi.debug.application"