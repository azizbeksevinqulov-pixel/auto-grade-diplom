import os

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "core",  # 👈 MUHIM (siz qo‘shgan app)
]

MIDDLEWARE = []

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}

STATIC_URL = "/static/"
