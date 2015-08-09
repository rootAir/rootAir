import os
import sys
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i+acxn5(akgsn!sr4^qgf(^m&*@+g1@u^t@=8s@axc41ml*f=s'


###########################################################
# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = (
    ('USER_NAME', 'USER_EMAIL'),
)

DOMAIN = 'YOUR_DOMAIN'
MANAGERS = ADMINS

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
REPOSITORY_ROOT = os.path.dirname(BASE_DIR)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
# STATIC_ROOT = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static'))
# STATIC_ROOT = os.path.join(REPOSITORY_ROOT, 'static/')
STATIC_ROOT = 'staticfiles'

STATIC_URL = '/static/'

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media'))
MEDIA_ROOT = os.path.join(REPOSITORY_ROOT, 'tmp/')

MEDIA_URL = '/tmp/'


# REST_FRAMEWORK = {
#                     'DEFAULT_PERMISSION_CLASSES': [
#                         'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
#                     ]
# }

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGE_SIZE': 10
}

###########################################################
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'location_field',
    'django_extensions',
    'activity',
    'finance',
    'travel',
    # 'djcelery',
    # 'crispy_forms',
    'broker',
    'rest_framework',
    # 'example.api',
    'hello',
    # 'utils',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

)

CRISPY_TEMPLATE_PACK = 'bootstrap3'


###########################################################
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Parse database configuration from $DATABASE_URL Enable Connection Pooling (if desired)
# DATABASE_URL = 'postgres://pwvoeyiyubbkeo:PbfoF02PJc9qQY-4VTDBtj2IQv@ec2-54-204-0-120.compute-1.amazonaws.com:5432/dbpri746ds51ev'
DATABASES['default'] =  dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django_postgrespool'
# DATABASES['default']['DATABASE_URL'] = DATABASE_URL
# DATABASES['default']['HEROKU_POSTGRESQL_VIOLET'] = DATABASE_URL


###########################################################
# Celery RabitQM Broker configuration for Celery
# http://ask.github.com/celery/getting-started/first-steps-with-django.html
# from celery.schedules import crontab

# CARROT_BACKEND = "amqp"   # deprecated
BROKER_BACKEND = "amqp"
CELERY_RESULT_BACKEND = "amqp" # ['database', 'amqp', 'redis://localhost:6379/0']
BROKER_POOL_LIMIT = 2
BROKER_HEARTBEAT = 30
CELERY_TASK_RESULT_EXPIRES = 18000
BROKER_CONNECTION_TIMEOUT = 30
CELERY_SEND_EVENTS = True
CELERY_EVENT_QUEUE_EXPIRE = 60

# BROKER_URL = 'redis://localhost:6379/0'
# BROKER_HOST = "hyena.rmq.cloudamqp.com"
RABBIT_URL = ''
CELERY_ALWAYS_EAGER = False  # manage runserver
# CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
# CELERY_IMPORTS = ('ChannelPromise',)  # List of modules to import when celery starts.
# CELERY_SEND_TASK_ERROR_EMAILS = True
# CELERYD_LOG_LEVEL = 'INFO'     #deprecated
# CELERYBEAT_LOG_LEVEL = 'INFO'  #deprecated
# CELERYD_PREFETCH_MULTIPLIER = 1

CELERY_ACCEPT_CONTENT = ['json']   # ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# HABBITMQ_PORT = 5672
# BROKER_VHOST = "xbblmfki"
# BROKER_USER = "xbblmfki"
# BROKER_PASSWORD = "HkmpvAPXFfVbp5O96PkvPj_7VHkuZZfm"
# RABBIT_URL = "amqp://guest:guest@localhost:5672/"

#commented to give a chance of settings being modified before djcelery setup
# import djcelery
# djcelery.setup_loader()

CELERY_QUEUE_SYNC_DB = "sync_db"
CELERY_QUEUE_ADD = "add"

###########################################################

# Application definition

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# AUTH_USER_MODEL = 'api.User'
#
# # !!!!!This is for demonstration only!!!!!
# AUTHENTICATION_BACKENDS = ['example.api.auth.AlwaysRootBackend']

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)

###########################################################

ROOT_URLCONF = 'rootair.urls'
# ROOT_URLCONF = 'example.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rootair.wsgi.application'

#Login Site
LOGIN_URL = "/"
LOGOUT_URL = "/logout/"
LOGIN_REDIRECT_URL = "/finance/"

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

#LANGUAGE_CODE = 'en-us'
#TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt-br'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# TEMPLATE_DIRS = (
#
#      os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static", "templates"),
# )

# TEMPLATE_DIRS = (
#     os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
# )
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "static", "templates"),
)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATICFILES_DIRS = (
    os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets')),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
DIR_LOCAL = '/Users/user/Dropbox/projects/rootAir-pack/robo_screenshot/'
CHROME_DRIVER = "/Users/user/Dropbox/projects/rootAir-pack/lib/chromedriver"
URL_DROPBOX = 'https://www.dropbox.com/home/%s'

# MyCap
MYCAP_USERNAME = 'YOUR_MYCAP_USERNAME'
MYCAP_PASSWORD = 'YOUR_MYCAP_PASSWORD'
HOUR_INIT_BROKER = '09:50'
HOUR_FINAL_BROKER = '16:30'
MIN_QUANT_PURCHASE = 100
MINUTE_FIND_TREND = 3
QUANT_FIND_ACTIVE = 4
VALUE_MAX_PURCHASE = 10

# Itau
ITAU_AGENCIA = 'YOUR_ITAU_AGENCIA'
ITAU_CONTA = 'YOUR_ITAU_CONTA'

# Google
EMAIL_GOOGLE = 'YOUR_EMAIL_GOOGLE'
SENHA_GOOGLE = 'YOUR_SENHA_GOOGLE'
DOC_KEY_GOOGLE = 'YOUR_DOC_KEY_GOOGLE'

# DataBase
DATABASE_REMOTE = 'heroku'
DATABASE_LOCAL = False
DOC_KEY_DATABASE = 'YOUR_DOC_KEY_DATABASE'

# Trello
TRELLO_BOARD = 'YOUR_TRELLO_BOARD'
TRELLO_API_KEY = 'YOUR_TRELLO_API_KEY'
TRELLO_API_SECRET = 'YOUR_TRELLO_API_SECRET'
TRELLO_TOKEN = 'YOUR_TRELLO_TOKEN'
TRELLO_TOKEN_SECRET = 'YOUR_TRELLO_TOKEN_SECRET'

# Dropbox
DEFAULT_FILE_STORAGE = URL_DROPBOX %'YOUR_DEFAULT_FILE_STORAGE'
DROPBOX_CONSUMER_KEY = 'YOUR_DROPBOX_CONSUMER_KEY'
DROPBOX_CONSUMER_SECRET = 'YOUR_DROPBOX_CONSUMER_SECRET'
DROPBOX_ACCESS_TOKEN = 'YOUR_DROPBOX_ACCESS_TOKEN'
DROPBOX_ACCESS_TOKEN_SECRET = 'YOUR_DROPBOX_ACCESS_TOKEN_SECRET'

TYPELAUNCH_DEFAULT = '(Nenhum)'


try:
    local = open(os.path.join(BASE_DIR,'settings_local.py')).read()
    exec(local)
except IOError:
	pass
