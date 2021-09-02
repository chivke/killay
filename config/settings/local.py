from .base import *  # noqa
from .base import env

# Local/dev settings

DEBUG = True
SECRET_KEY = env(
    "DJANGO_SECRET_KEY", default="vkm6AHf9Giw8TQsNWfPBft5L1Y6oycu0WAz5gGhUq"
)
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache" ".backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# MailDev
# https://github.com/maildev/maildev

EMAIL_HOST = "maildev"
EMAIL_PORT = 25

INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects" ".RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS += ["django_extensions"]  # noqa F405

# CORS_ALLOWED_ORIGINS = ['http://localhost:8080']
