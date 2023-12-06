# Base settings
import os

from pathlib import Path

import environ


ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = ROOT_DIR / "killay"
environ.Env.read_env(os.path.join(ROOT_DIR, ".env"))
env = environ.Env()

# General

DEBUG = env.bool("DJANGO_DEBUG", default=False)
LANGUAGE_CODE = "en-us"
SITE_ID = 1
USE_TZ = True
SITE_NAME = env("SITE_NAME", default="Killay Site Name")
SITE_DOMAIN = env("SITE_DOMAIN", default="killay-site.com")
LOCALE_PATHS = (str(ROOT_DIR / "locale"),)

# Database

DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["OPTIONS"] = {
    "sql_mode": "traditional",
    "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
}
# URLs

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# Apps

DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
]

THIRD_PARTY_APPS = ["django_quill"]

LOCAL_APPS = [
    "killay.users.apps.UsersConfig",
    "killay.pages.apps.PagesConfig",
    "killay.videos.apps.VideosConfig",
    "killay.admin.apps.AdminConfig",
    "killay.archives.apps.ArchivesConfig",
    "killay.viewer.apps.ViewerConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Authentication

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "users:redirect"
LOGOUT_REDIRECT_URL = "users:login"
LOGIN_URL = "users:login"

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# Middleware

LOCAL_MIDDLEWARE = [
    "killay.admin.middleware.SiteConfigurationMiddleware",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    *LOCAL_MIDDLEWARE,
]

# Static

STATIC_ROOT = str(ROOT_DIR / "static")
STATIC_URL = env("STATIC_URL", default="/static/")
STATICFILES_DIRS = [str(APPS_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Media

MEDIA_ROOT = str(APPS_DIR / "media")
MEDIA_URL = env("MEDIA_URL", default="/media/")

# Template

CUSTOM_CONTEXT_PROCESSORS = [
    "killay.admin.context_processors.site_context",
    "killay.pages.context_processors.pages_context",
    "killay.videos.context_processors.collections_context",
    "killay.viewer.context_processors.general_context",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates"), str(APPS_DIR / "admin" / "templates")],
        "OPTIONS": {
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                *CUSTOM_CONTEXT_PROCESSORS,
            ],
        },
    }
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"


# Fixtures

FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# Security

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "SAMEORIGIN"

# Email

EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_TIMEOUT = 5

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# Quill HTML input

QUILL_CONFIGS = {
    "default": {
        "theme": "snow",
        "modules": {
            "syntax": True,
            "toolbar": [
                [
                    {"header": []},
                    {"align": []},
                    "bold",
                    "italic",
                    "underline",
                    "strike",
                    "blockquote",
                    {"color": []},
                    {"background": []},
                ],
                ["code-block", "link"],
                ["clean"],
            ],
        },
    }
}
