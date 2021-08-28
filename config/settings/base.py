from django.conf import settings
import os
import dotenv
import subprocess
import configparser


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 서버 log 저장 코드
LOG_DIR = "/var/log/django"

if not os.path.exists(LOG_DIR):
    LOG_DIR = os.path.join(BASE_DIR, ".log")
    os.makedirs(LOG_DIR, exist_ok=True)

subprocess.call(["chmod", "755", LOG_DIR])

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "django.server": {
            "format": "[%(asctime)s] %(message)s",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "file_error": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "django.server",
            "backupCount": 10,
            "filename": os.path.join(LOG_DIR, "error.log"),
            "maxBytes": 10485760,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file_error"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "*",
]


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

PICKY_APPS = [
    "editor_reviews.apps.EditorReviewsConfig",
    "products.apps.ProductsConfig",
    "comments.apps.CommentsConfig",
    "users.apps.UsersConfig",
    "core.apps.CoreConfig",
    "orders.apps.OrdersConfig",
    "farmers.apps.FarmersConfig",
    "admins.apps.AdminsConfig",
    "likes.apps.LikesConfig",
    "django_summernote",
    "addresses.apps.AddressesConfig",
    "django_seed",
    "storages",
    "kakaomessages",
]

INSTALLED_APPS = PICKY_APPS + DJANGO_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

X_FRAME_OPTIONS = "SAMEORIGIN"

ROOT_URLCONF = "config.urls"

SUMMERNOTE_CONFIG = {
    "iframe": True,
    "airMode": True,
    "width": "990px",
    "height": "661px",
    "toolbar": [
        # ['style', ['style']],
        [
            "font",
            [
                "bold",
                "italic",
                "underline",
                "superscript",
                "subscript",
                "strikethrough",
                "clear",
            ],
        ],
        # ['fontname', ['fontname']],
        ["fontsize", ["fontsize"]],
        # ['color', ['color']],
        ["para", ["ul", "ol", "paragraph"]],
        ["height", ["height"]],
        ["table", ["table"]],
        ["insert", ["link", "picture", "video", "hr"]],
        ["view", ["fullscreen", "codeview"]],
        ["help", ["help"]],
    ],
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# # Database
# # https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_L10N = True

USE_TZ = True

### User Setting
AUTH_USER_MODEL = "users.User"
LOGIN_URL = "/user/login/"

### Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_devs"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

### Media files
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


### Email 전송
# 메일을 호스트하는 서버
EMAIL_HOST = os.environ.get("EMAIL_HOST")

# gmail과의 통신하는 포트
EMAIL_PORT = os.environ.get("EMAIL_PORT")

# 발신할 이메일
# EMAIL_HOST_USER = '구글아이디@gmail.com'
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")

# 발신할 메일의 비밀번호
# EMAIL_HOST_PASSWORD = '구글비밀번호'
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

# TLS 보안 방법
EMAIL_USE_TLS = True

# 사이트와 관련한 자동응답을 받을 이메일 주소
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# kakao 알림톡 SDK
apiKey = os.environ.get("api_key")
apiSecret = os.environ.get("api_secret")
protocol = os.environ.get("protocol")
domain = os.environ.get("domain")
prefix = os.environ.get("prefix") and os.environ.get("prefix") or ""


def getUrl(path):
    url = "%s://%s" % (protocol, domain)
    if prefix != "":
        url = url + prefix
    url = url + path
    return url
