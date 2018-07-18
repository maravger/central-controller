"""
Django settings for central_controller project.

Generated by 'django-admin startproject' using Django 1.11.14.

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
SECRET_KEY = '3)0_7qe*a9zdsc^hmc++nf0)&qts@nu@ek*%o76c)#)ptql*b@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["0.0.0.0", "10.11.16.112"]

GLOBAL_SETTINGS = {
    'SAMPLING_INTERVAL': 30.0,
    'APPS': [0, 1],
    'HOST_IPS': ['10.11.17.9', '10.11.17.10'],
    'U_PES_MIN': [[0, 0.10, 0.20, 0.30, 0.40], [0, 0.10, 0.20, 0.30, 0.40]],
    'U_PES_MAX': [[0, 0.30, 0.40, 0.50, 0.60], [0, 0.30, 0.40, 0.50, 0.60]],
    'U_REQ_MIN': [[0, 0.5, 3.5, 4.5, 5.5], [0, 0.5, 3.5, 4.5, 5.5]],
    'U_REQ_MAX': [[0, 3.5, 5.5, 7.5, 10], [0, 3.5, 5.5, 7.5, 10]],
    'X_ART_REF': [[0, 2.5, 2.5, 2.5, 2.5], [0, 3.5, 3.5, 3.5, 3.5]],
    'U_PES_REF': [[0, 0.25, 0.35, 0.45, 0.55], [0, 0.25, 0.35, 0.45, 0.55]],
    'U_REQ_REF': [[0, 2.9522, 4.6272, 6.1769, 8.0228], [0, 3.2358, 5.2899, 7.375, 9.5755]],
    'K1': [[0, 0, 0, 0, 0.84874], [0, 1.4286, 0, 0, 0.61825]],
    'K2': [[0, -0.21913, -0.34912, -0.52926, -0.79089], [0, -0.075496, -0.060028, -0.035707, -0.1213]],
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'central_controller.urls'

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

WSGI_APPLICATION = 'central_controller.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# Celery application definition
# http://docs.celeryproject.org/en/v4.0.2/userguide/configuration.html
# CELERY_WORKER_HIJACK_ROOT_LOGGER = False
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Athens'
CELERY_BEAT_SCHEDULE = {
    'scale-horizontally': {
        'task': 'api.tasks.horizontal_scaler.scale_horizontally',
        'schedule': GLOBAL_SETTINGS['SAMPLING_INTERVAL']
    }
}