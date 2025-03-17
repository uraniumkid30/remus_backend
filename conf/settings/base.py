import os
from dotenv import load_dotenv
from conf.addons.constants import *
from conf.addons.directories import (
    THEME_DIR,
    LOGS_DIR,
    BASE_DIR,
    DIRECT_MEDIA_DIR,
    MEDIA_DIR,
    PDF_FONTS_DIR,
    ARCHIVE_DIR
)

from conf.addons.apps import INSTALLED_APPS, LOCAL_APPS
from conf.addons.logs import get_logs_settings
from conf.addons.public_exports import *


LOGIN_URL = "/login/"
LOGOUT_URL = "/logout/"

ANONYMOUS_URLS = [
    r"^admin/$",
    r"^admin/login/$",
    r"^media/",
    r"^static/",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "conf.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(THEME_DIR, "templates")],
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

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin,
    "applications.accounts.managers.backends.SettingsBackend",
    "django.contrib.auth.backends.ModelBackend",
]

LOGGING = get_logs_settings(LOGS_DIR, LOCAL_APPS)
AUTH_USER_MODEL = "accounts.User"
API_VERSION = "v1"
