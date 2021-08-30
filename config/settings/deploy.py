from .base import *
import os

DEBUG = False
ALLOWED_HOSTS = ["*"]


# WSGI application
WSGI_APPLICATION = "config.wsgi.deploy.application"

### S3 설정
DEFAULT_FILE_STORAGE = "config.asset_storage.S3DefaultStorage"
# STATICFILES_STORAGE = "config.asset_storage.S3StaticStorage"

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

AWS_REGION = "ap-northeast-2"
AWS_STORAGE_BUCKET_NAME = "pickyfarm"
AWS_S3_CUSTOM_DOMAIN = "%s.s3.%s.amazonaws.com" % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

# RDS Setting
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "HOST": os.environ.get("RDS_ENDPOINT_URL"),
#         "PORT": os.environ.get("RDS_CONNECTION_PORT"),
#         "NAME": os.environ.get("RDS_SCHEMA_NAME"),
#         "USER": os.environ.get("RDS_CLIENT_NAME"),
#         "PASSWORD": os.environ.get("RDS_CONNECT_PW"),
#     }
# }

# AWS_LOCATION = "static"
# STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
