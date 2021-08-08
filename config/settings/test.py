from .base import *  # noqa
from .base import env

SECRET_KEY = env('DJANGO_SECRET_KEY',
                 default='vkm6AHf9Giw8TQsNWfPBft5L1Y6oycu0WAz5gGhUq')

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

CACHES = {'default': {'BACKEND': 'django.core.cache.backends'
                                 '.locmem.LocMemCache',
                      'LOCATION': ''}}

PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
TEMPLATES[-1]['OPTIONS']['loaders'] = [  # noqa F405
    (
        'django.template.loaders.cached.Loader',
        [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ],
    )
]

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'


SLACK_TEST_USER_ID = env('SLACK_TEST_USER_ID', default='U01GVMYAGG2')
