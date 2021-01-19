"""
Django settings for devops project.

Generated by 'django-admin startproject' using Django 1.11.16.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(BASE_DIR, "apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9vg^(z0ay7ii873g1!7--##r(r#=iisz3wn@mzkxbmx_5iw7))'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'users.User'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'groupUsers',
    'users',
    'corsheaders',
    'resources',
    'django_apscheduler',
    'django_filters'
]
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:8080',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'devops.urls'

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

WSGI_APPLICATION = 'devops.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'devops',
		'USER': 'root',
		'PASSWORD': '123456',
		'HOST': '127.0.0.1',
		'PORT': 3306,
		'OPTIONS':{
			'init_command': 'SET default_storage_engine=INNODB;',
		},
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

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

from rest_framework.settings import api_settings

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'devops.paginations.Pagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
}

## qcloud
QCLOUD_SECRETID = "AKIDFaq5EbGxiQx22qzUL2XtCJJ7j9NQuyTq"
QCLOUD_SECRETKEY = "LTP8fz72lOr8D8reFerunUyGQN7f4LTP"

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'loggers': {
#         'reboot': {
#             'handlers': ["reboot"],
#             'level': 'DEBUG',
#             'propagate': True
#         },
#         "django": {
#             'handlers': ["django"],
#             'level': 'DEBUG',
#             'propagate': True
#         },
#         "django.server": {
#             'handlers': ["django_server"],
#             'level': 'DEBUG',
#             "propagate": True
#         }
#     },
#     'handlers': {
#         'reboot': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple',
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/tmp/django.log',
#             'formatter': 'json',
#         },
#         'django': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/tmp/default.log',
#             'formatter': 'simple',
#         },
#         'django_server': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/tmp/django_server.log',
#             'formatter': 'simple',
#         },
#     },
#     'formatters': {
#         'json': {
#             'format': '{"levelname":"%(levelname)s","asctime":"%(asctime)s","module":"%(name)s","fullpath":"%(pathname)s","funcName":"%(funcName)s","lineno":"%(lineno)s","message":"%(message)s"}'
#         },
#         'reboot': {
#             'format': '%(asctime)s - %(pathname)s:%(lineno)d[%(levelname)s] - %(message)s'
#         },
#         'simple': {
#             'format': '%(name)s %(asctime)s %(levelname)s %(message)s'
#         },
#         'verbose': {
#             'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
#         },
#     },
#     "root": {
#         'handlers': ["file"],
#         'level': 'DEBUG',
#     }
# }
