import os  # isort:skip
gettext = lambda s: s
DATA_DIR = os.path.dirname(os.path.dirname(__file__))
"""
Django settings for archivopirke project.

Generated by 'django-admin startproject' using Django 1.11.23.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#$ pwgen 45 1 > secretkey.txt
#
#
#   
#

SECRET_DEPLOY = False

if not SECRET_DEPLOY:
    SECRET_KEY = '0r$(2w%t!b4dub)(n45*(td09$ffwn14w-6c%ec+^4=zgypm7='
else:
    with open('secretkey.txt') as f:
        SECRET_KEY = f.read().strip()

DEBUG = True

# Database in dev (true) or deploy (false)
#$ sed -i 's/DB_DEBUG = True/DB_DEBUG= False/g' settings.py
DB_DEBUG = True

if DB_DEBUG:
    DATABASES = {
        'default': {
            'CONN_MAX_AGE': 0,
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'project.db',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
else:
#$ postgres user password in secretkey_db.txt
    with open('secretkey_db.txt') as f:
        DATABASES = {
            'default': {
                'CONN_MAX_AGE': 0,
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'cmpirque',
                'HOST': 'localhost',
                'PASSWORD': f.read().strip(),
                'PORT': '5432',  
                'USER': 'cmpirque'
            }
        }

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']
#CSRF_COOKIE_SECURE = True
#SESSION_COOKIE_SECURE = True


# Application definition

ROOT_URLCONF = 'archivopirke.urls'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
#MEDIA_URL = '../data/media/'
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
STATIC_ROOT = os.path.join(DATA_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'archivopirke', 'static'),
)
SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'archivopirke', 'templates'),],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.template.context_processors.static',
                'cms.context_processors.cms_settings'
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader'
            ],
        },
    },
]

#X_FRAME_OPTIONS = 'DENY'
#SECURE_CONTENT_TYPE_NOSNIFF = True
#SECURE_BROWSER_XSS_FILTER = True


MIDDLEWARE = [
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware'
]

INSTALLED_APPS = [
    'djangocms_admin_style',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'filer',
    'easy_thumbnails',
    'djangocms_column',
    'djangocms_file',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_style',
    'djangocms_snippet',
    'djangocms_googlemap',
    'archivopirke',
    'videolog',
    'djangocms_video',
]

LANGUAGES = (
    ## Customize this
    ('es', gettext('es')),
)

CMS_LANGUAGES = {
    ## Customize this
    1: [
        {
            'code': 'es',
            'hide_untranslated': False,
            'redirect_on_fallback': True,
            'name': gettext('es'),
            'public': True,
        },
    ],
    'default': {
        'redirect_on_fallback': True,
        'public': True,
        'hide_untranslated': False,
    },
}

CMS_TEMPLATES = (
    ## Customize this
    ('page.html', 'Page'),
    ('feature.html', 'Page with Feature'),
    ('home.html', 'Home template'),
    ('proyecto.html', 'Proyecto template'),
)

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {
    'video': {
        'plugins': ['VideoPlayerPlugin'],
        'default_plugins': [
            {
                'plugin_type': 'VideoPlayerPlugin',
                'values': {'label':'video'}
            }
        ]
    }
}

MIGRATION_MODULES = {
    
}

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

LOGIN_REDIRECT_URL = '/admin'
LOGOUT_REDIRECT_URL = '/'
