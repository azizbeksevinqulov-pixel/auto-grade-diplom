import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# ===================== SECURITY =====================
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

DEBUG = False

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "https://*.railway.app"
]


# ===================== APPS =====================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "core",
]


# ===================== MIDDLEWARE =====================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",   # ← Yangi qator
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]


# ===================== URL / WSGI =====================
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"


# ===================== DATABASE =====================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ===================== CUSTOM USER =====================
AUTH_USER_MODEL = "core.CustomUser"


# ===================== TEMPLATES =====================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # agar template ishlatsangiz
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


# ===================== STATIC FILES =====================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


# ===================== AUTH REDIRECT =====================
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/test/"   # oldin dashboard edi → endi test
LOGOUT_REDIRECT_URL = "/login/"


# ===================== SECURITY (PRODUCTION) =====================
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
