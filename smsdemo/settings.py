"""
Django settings for smsdemo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '@w0^p@xah19_(o!*$vrvoh^7!)6)@_m=^0(2q&5$a==+b=&q$y')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'SECRET_KEY' not in os.environ

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(';')


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # External apps
    'django_tables2',
    'selectable',
    # RapidSMS
    'rapidsms',
    'rapidsms.contrib.handlers',
    'rapidsms.contrib.messagelog',
    'rtwilio',
    'smsgroups',
)

INSTALLED_BACKENDS = {}

RAPIDSMS_HANDLERS = (
    'smsgroups.handlers.create_group.CreateHandler',
    'smsgroups.handlers.join_group.JoinHandler',
    'smsgroups.handlers.msg_group.BroadcastHandler',
)

if DEBUG:
    INSTALLED_APPS += (
        'rapidsms.backends.database',
        'rapidsms.contrib.httptester',
    )

    INSTALLED_BACKENDS['message_tester'] = {
        'ENGINE': 'rapidsms.backends.database.DatabaseBackend',
    }

    RAPIDSMS_HANDLERS += (
        'rapidsms.contrib.echo.handlers.echo.EchoHandler',
        'rapidsms.contrib.echo.handlers.ping.PingHandler',
    )

if all('TWILIO_%s' % name in os.environ for name in ['ACCOUNT_SID', 'AUTH_TOKEN', 'NUMBER']):
    INSTALLED_BACKENDS['twilio-backend'] = {
        'ENGINE': 'rtwilio.outgoing.TwilioBackend',
        'config': {
            'account_sid': os.environ['TWILIO_ACCOUNT_SID'],
            'auth_token': os.environ['TWILIO_AUTH_TOKEN'],
            'number': os.environ['TWILIO_NUMBER'],
        }
    }

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'smsdemo.urls'

WSGI_APPLICATION = 'smsdemo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default='postgres:///smsdemo'),
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)
