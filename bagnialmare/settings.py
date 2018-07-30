# Django settings for bagnialmare project.
import os

from .basesettings import DB_NAME
from .basesettings import DB_PASSWORD
from .basesettings import DB_USER
from .basesettings import DEVELOPMENT
from .basesettings import DJANGO_ROOT_URL
from .basesettings import DJANGO_SECRET_KEY
from .basesettings import DJANGO_WSGI_APPLICATION
from .basesettings import HOST_NAME
from .basesettings import SMTP_HOST
from .basesettings import SMTP_PASSWORD
from .basesettings import SMTP_USER

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': 'db',
        'PORT': '',
    }
}

ALLOWED_HOSTS = [HOST_NAME, ]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEVELOPMENT

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJ_DIR)


TEMPLATE_DEBUG = DEVELOPMENT
COMPRESS_ENABLED = not DEVELOPMENT

SITE_ID = 1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_SECRET_KEY
ROOT_URLCONF = DJANGO_ROOT_URL

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = DJANGO_WSGI_APPLICATION

DEFAULT_FROM_EMAIL = "info@bagnialmare.com"
ACCOUNT_SIGNUP_FORM_CLASS = "authauth.forms.ManagerSignupForm"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_DISPLAY = "authauth.models.display_user"
LOGIN_REDIRECT_URL = "homepage"

if not DEVELOPMENT:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': 'memcached:11211',
            'OPTIONS': {
                'MAX_ENTRIES': 2000
            }
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

ADMINS = (
    ("Matteo Parrucci", "parruc@gmail.com", ),
    ("Nicola Valentini", "nicola.valentini@gmail.com", ),
    ("Marco Bartolini", "marcobartolini@gmail.com", ),
    ("Marco Benvenuto", "marco.benvenuto1@gmail.com", ),
    ("Bagnialmare", "info@bagnialmare.com", ),
)

MANAGERS = ADMINS

WHOOSH_INDEX = os.path.join(os.path.dirname(__file__), 'whoosh_index')

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#\wed-hosts
ALLOWED_HOSTS = [HOST_NAME, ]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Rome'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en' #default lnguage?!?

MODELTRANSLATION_AUTO_POPULATE = 'all'

gettext = lambda s: s

LANGUAGES = (
    ('en', gettext('English')),
    ('it', gettext('Italiano')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/media/'


# Additional locations of static files
STATICFILES_DIRS = [
    os.path.normpath(os.path.join(PROJ_DIR, "static")),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

FIXTURE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'fixtures'),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)

TEMPLATE_DIRS = (
    '/project/bagnialmare/bagnialmare/templates',
)

LOCALE_PATHS = (
    '/project/bagnialmare/bagnialmare/locale/',
    '/project/bagnialmare/authauth/locale/',
    '/project/bagnialmare/bagni/locale/',
    '/project/bagnialmare/booking/locale/',
    '/project/bagnialmare/contacts/locale/',
)

INSTALLED_APPS = [
    'bagni',
    'booking',
    'newsletters',
    'multilingual',
    'authauth',
    'contacts',
    'userfeedback',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'autoslug',
    'compressor',
    'ckeditor',
    'modeltranslation',
    'sorl.thumbnail',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.gis',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.webdesign',
]
if DEVELOPMENT:
    INSTALLED_APPS.append('debug_toolbar')
# South specific configuration to exclude migrations from tests
SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False

if DEVELOPMENT:
    MANDRILL_API_KEY = "oqrObEV8ZI_4hvxcNwbDcQ"
    MANDRILL_API_TEST_KEY = "9A8CJujchIFopMGY0Xry8A"
    MASS_EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    MASS_EMAIL_TEST_BACKEND  = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = "/var/log/django/email"
else:
    MANDRILL_API_KEY = "oqrObEV8ZI_4hvxcNwbDcQ"
    MANDRILL_API_TEST_KEY = "9A8CJujchIFopMGY0Xry8A"
    MASS_EMAIL_BACKEND = "newsletters.mail.backends.mandrill.MandrillBackend"
    MASS_EMAIL_TEST_BACKEND = "newsletters.mail.backends.mandrill.MandrillTestBackend"
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = SMTP_HOST
EMAIL_PORT = 465
EMAIL_HOST_USER = SMTP_USER
EMAIL_HOST_PASSWORD = SMTP_PASSWORD
EMAIL_USE_SSL = True

# TODO: Configurare il mule uwsgi per fare questo lavoro
# MAILOFFLOADER_SOCKET = "ipc:///tmp/mailoffloader.ipc"

#this must be defined but ckeditor uploads are disabled
#without this variable django will not work thus
CKEDITOR_UPLOAD_PATH = "ckuploads/"
CKEDITOR_CONFIGS = {
    'default' : {
        'toolbar': 'Basic',
        'removeButtons': 'Source',
    },
    'admin' : {
       'toolbar': 'Full',
    },
}


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

if DEVELOPMENT:
    LOGGING["handlers"]["file"] = {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/django.log',
    }
    LOGGING["loggers"]["django"]["handlers"].append("file")
