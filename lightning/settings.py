# Django settings for lightning project.

import os
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

from settings_private import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Kevin Xu', 'kevin@imkevinxu.com'),
    ('Wylie Conlon', 'lightning@wylie.su'),
)

MANAGERS = ADMINS

# DATABASES is set in settings_private.py

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
### Set to None so that Django will use the same timezone as the os. This is
### specific to Unix based-systems. Read above ^
TIME_ZONE = 'America/Los_Angeles'
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, "media/")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, "static/")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = 'http://s3.amazonaws.com/lightning-app/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Serve static files from S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Set in settings_private.py

# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
# AWS_STORAGE_BUCKET_NAME

# EMAIL_HOST
# EMAIL_HOST_USER
# EMAIL_HOST_PASSWORD
# EMAIL_PORT
# EMAIL_USE_TLS

# SENDGRID_FROM

# TWILIO_FROM
# TWILIO_ACCOUNT
# TWILIO_TOKEN

# FIVEHUNDRED_CONSUMER_KEY

# SECRET_KEY

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'lightning.urls'

WSGI_APPLICATION = 'lightning.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates/'),
)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
)

AUTH_PROFILE_MODULE = 'lightning_app.UserProfile'

LOGIN_REDIRECT_URL = '/login_redirect'

# Uncomment any apps you want to use. We will not
# install all apps by default, but all of the
# commented apps are one's we "should" be using.

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    ####
    # 'sentry',
    # 'djcelery',
    # 'mptt',
    # 'raven.contrib.django',
    'storages',
    'south',
    'lightning_app',

)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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

####
# import local settings overriding the defaults
####
if not os.environ.get('PRODUCTION', False):
    try:
        from settings_local import *
    except ImportError:
        try:
            from mod_python import apache
            apache.log_error( "local settings not available", apache.APLOG_NOTICE )
        except ImportError:
            import sys
            sys.stderr.write( "local settings not available\n" )
    else:
        try:
            INSTALLED_APPS += LOCAL_INSTALLED_APPS
        except NameError:
            pass


# Heroku is supposed to inject this code.... for some reason it doesn't
# TODO: Look into why Heroku isn't
# http://stackoverflow.com/questions/10596893/deploying-django-to-heroku-psycopg2-error
import sys
import urlparse
import os


# Register database schemes in URLs.
urlparse.uses_netloc.append('postgres')
urlparse.uses_netloc.append('mysql')

try:

    # Check to make sure DATABASES is set in settings.py file.
    # If not default to {}

    if 'DATABASES' not in locals():
        DATABASES = {}

    if 'DATABASE_URL' in os.environ:
        url = urlparse.urlparse(os.environ['DATABASE_URL'])

        # Ensure default database exists.
        DATABASES['default'] = DATABASES.get('default', {})

        # Update with environment configuration.
        DATABASES['default'].update({
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
        })
        if url.scheme == 'postgres':
            DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

        if url.scheme == 'mysql':
            DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
except Exception:
    print 'Unexpected error:', sys.exc_info()
