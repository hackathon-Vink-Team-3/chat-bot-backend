import os
from pathlib import Path

from environs import Env

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# base
INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# packages
INSTALLED_APPS += [
    "channels",
    "rest_framework",
    "drf_yasg",
    "corsheaders",
]

# apps
INSTALLED_APPS += [
    "src.apps.users",
    "src.apps.api",
    "src.apps.chat",
    "src.apps.tg_bot",
    "src.apps.core",
]

# logging
LOG_DIR = os.path.join(BASE_DIR, ".logs")
LOG_FILE = "/main.log"
LOG_PATH = LOG_DIR + LOG_FILE

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

if not os.path.exists(LOG_PATH):
    f = open(LOG_PATH, "a").close()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "[-{levelname}- {asctime}] :: {pathname} :: {module} :: {funcName} :: {message}",  # noqa
            "style": "{",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",  # noqa
            "format": "{levelname}{asctime}{pathname}{module}{funcName}{message}",  # noqa
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "WARNING" if DEBUG else "INFO",
            "class": "logging.FileHandler",
            "filename": LOG_PATH,
            "formatter": "json",
        },
        "stream": {
            "level": "DEBUG" if DEBUG else "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "loggers": {
        "src.apps.tg_bot": {
            "handlers": ["file", "stream"],
            "level": "DEBUG",
            "propagate": True,
        },
        "src.apps.chat": {
            "handlers": ["file", "stream"],
            "level": "DEBUG",
            "propagate": True,
        },
        "src.apps.core": {
            "handlers": ["file", "stream"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


DATABASES = {
    "default": {
        "ENGINE": env.str("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": env.str("POSTGRES_DB", "django"),
        "USER": env.str("POSTGRES_USER", "django"),
        "PASSWORD": env.str("POSTGRES_PASSWORD", ""),
        "HOST": env.str("DB_HOST", ""),
        "PORT": env.int("DB_PORT", 5432),
    }
}


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

AUTH_USER_MODEL = "users.CustomUser"


LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
}


CORS_ORIGIN_ALLOW_ALL = True  # Изменить на проде
CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_SAMESITE = None
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")


# tg_bot_settings
BOT_TOKEN = env.str("TG_BOT_TOKEN")
WEBHOOK_SECRET = env.str("WEBHOOK_SECRET")
WEBHOOK_URL = env.str("WEBHOOK_URL")

# swagger
SWAGGER_SETTINGS = {
    "DEFAULT_AUTO_SCHEMA_CLASS": "src.apps.api.swagger_schema.CustomAutoSchema",
}

# constants
MAX_LEN_MESSAGE_TEXT_FIELD = 2000
ASSESSMENT_MAX_VALUE = 10
ASSESSMENT_MIN_VALUE = 1
MAX_LEN_SENDER_TYPE = 7
MAX_LEN_PHONE_NUMBER = 12
MAX_LEN_USERNAME = 150

# redis
REDIS_HOST = env.str("REDIS_HOST")

# yagpt
YA_API_URL = env.str("YA_API_URL")
MODEL_API_KEY = env.str("MODEL_API_KEY")


try:
    from .local_settings import *
except ImportError:
    pass
