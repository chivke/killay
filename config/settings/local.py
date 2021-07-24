from .base import *  # noqa
from .base import env

# Local/dev settings

DEBUG = True
SECRET_KEY = env('DJANGO_SECRET_KEY',
                 default='vkm6AHf9Giw8TQsNWfPBft5L1Y6oycu0WAz5gGhUq')
ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1']

CACHES = {'default': {'BACKEND': 'django.core.cache'
                                 '.backends.locmem.LocMemCache',
                      'LOCATION': ''}}
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.console.EmailBackend')
INSTALLED_APPS += ['debug_toolbar']  # noqa F405
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']  # noqa F405
DEBUG_TOOLBAR_CONFIG = {'DISABLE_PANELS': ['debug_toolbar.panels.redirects'
                                           '.RedirectsPanel'],
                        'SHOW_TEMPLATE_CONTEXT': True}
INTERNAL_IPS = ['127.0.0.1']
# if env('USE_DOCKER') == 'yes':
#    import socket#
#
#    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
#    INTERNAL_IPS += ['.'.join(ip.split('.')[:-1] + ['1']) for ip in ips]

INSTALLED_APPS += ['django_extensions']  # noqa F405
CELERY_TASK_EAGER_PROPAGATES = True
# CORS_ALLOWED_ORIGINS = ['http://localhost:8080']
