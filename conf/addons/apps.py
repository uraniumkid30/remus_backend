import functools


DEFAULT_APPS = [
    "admin_notification",
    "admin_tools_stats",  # this must be BEFORE 'admin_tools' and 'django.contrib.admin'
    "django_nvd3",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
LOCAL_APPS = [
    "applications.accounts",
    "applications.merchant",
    "applications.wallet",
    "applications.location",
    "applications.administrator",
    "applications.cart",
    "applications.product",
    "applications.order",
    "applications.reviews",
    "applications.payment",
    "applications.general_services",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "rangefilter",
    "crispy_forms",
    "crispy_bootstrap5",
]

ALL_APPS_CONTAINER = {
    "DEFAULT_APPS": DEFAULT_APPS,
    "LOCAL_APPS": LOCAL_APPS,
    "THIRD_PARTY_APPS": THIRD_PARTY_APPS,
}

# Application definition
INSTALLED_APPS: list = functools.reduce(lambda x, y: x + y, ALL_APPS_CONTAINER.values())
