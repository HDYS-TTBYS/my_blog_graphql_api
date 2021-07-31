"""
Django settings for graphql_api project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from decouple import config
from dj_database_url import parse as dburl
from datetime import timedelta
from django.conf import settings as django_settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['my-blog-api-01.herokuapp.com', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users.apps.UsersConfig',
    'blog.apps.BlogConfig',

    "graphene_django",
    "graphql_jwt.refresh_token.apps.RefreshTokenConfig",
    "graphql_auth",
    "django_filters",
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

ROOT_URLCONF = 'graphql_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'graphql_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

default_dburl = 'sqlite:///' + str(BASE_DIR / "db.sqlite3")

DATABASES = {
    'default': config('DATABASE_URL', default=default_dburl, cast=dburl),
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR / 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

GRAPHENE = {
    "SCHEMA": "graphql_api.schema.schema",
    "MIDDLEWARE": ["graphql_jwt.middleware.JSONWebTokenMiddleware"],
}

AUTHENTICATION_BACKENDS = [
    "graphql_auth.backends.GraphQLAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
]

GRAPHQL_JWT = {
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.relay.Register",
        "graphql_auth.relay.VerifyAccount",
        "graphql_auth.relay.ResendActivationEmail",
        "graphql_auth.relay.SendPasswordResetEmail",
        "graphql_auth.relay.PasswordReset",
        "graphql_auth.relay.ObtainJSONWebToken",
        "graphql_auth.relay.VerifyToken",
        "graphql_auth.relay.RefreshToken",
        "graphql_auth.relay.RevokeToken",
        "graphql_auth.relay.VerifySecondaryEmail",
    ],
}

GRAPHQL_AUTH = {
    # if allow to login without verification,
    # the register mutation will return a token
    "ALLOW_LOGIN_NOT_VERIFIED": True,
    # mutations fields options
    "LOGIN_ALLOWED_FIELDS": ["email"],
    "ALLOW_LOGIN_WITH_SECONDARY_EMAIL": False,
    # required fields on register, plus password1 and password2,
    # can be a dict like UPDATE_MUTATION_FIELDS setting
    "REGISTER_MUTATION_FIELDS": ["email", "username"],
    "REGISTER_MUTATION_FIELDS_OPTIONAL": [],
    # optional fields on update account, can be list of fields
    "UPDATE_MUTATION_FIELDS": {"username": "String"},
    # tokens
    "EXPIRATION_ACTIVATION_TOKEN": timedelta(days=7),
    "EXPIRATION_PASSWORD_RESET_TOKEN": timedelta(hours=1),
    "EXPIRATION_SECONDARY_EMAIL_ACTIVATION_TOKEN": timedelta(hours=1),
    "EXPIRATION_PASSWORD_SET_TOKEN": timedelta(hours=1),
    # email stuff
    "EMAIL_FROM": getattr(django_settings, "DEFAULT_FROM_EMAIL", "test@email.com"),
    "SEND_ACTIVATION_EMAIL": True,
    # client: example.com/activate/token
    "ACTIVATION_PATH_ON_EMAIL": "activate",
    "ACTIVATION_SECONDARY_EMAIL_PATH_ON_EMAIL": "activate",
    # client: example.com/password-set/token
    "PASSWORD_SET_PATH_ON_EMAIL": "password-set",
    # client: example.com/password-reset/token
    "PASSWORD_RESET_PATH_ON_EMAIL": "password-reset",
    # email subjects templates
    "EMAIL_SUBJECT_ACTIVATION": "email/activation_subject.txt",
    "EMAIL_SUBJECT_ACTIVATION_RESEND": "email/activation_subject.txt",
    "EMAIL_SUBJECT_SECONDARY_EMAIL_ACTIVATION": "email/activation_subject.txt",
    "EMAIL_SUBJECT_PASSWORD_SET": "email/password_set_subject.txt",
    "EMAIL_SUBJECT_PASSWORD_RESET": "email/password_reset_subject.txt",
    # email templates
    "EMAIL_TEMPLATE_ACTIVATION": "email/activation_email.html",
    "EMAIL_TEMPLATE_ACTIVATION_RESEND": "email/activation_email.html",
    "EMAIL_TEMPLATE_SECONDARY_EMAIL_ACTIVATION": "email/activation_email.html",
    "EMAIL_TEMPLATE_PASSWORD_SET": "email/password_set_email.html",
    "EMAIL_TEMPLATE_PASSWORD_RESET": "email/password_reset_email.html",
    "EMAIL_TEMPLATE_VARIABLES": {},
    # query stuff
    "USER_NODE_EXCLUDE_FIELDS": ["password", "is_superuser"],
    "USER_NODE_FILTER_FIELDS": {
        "email": ["exact"],
        "username": ["exact", "icontains", "istartswith"],
        "is_active": ["exact"],
        "status__archived": ["exact"],
        "status__verified": ["exact"],
        "status__secondary_email": ["exact"],
    },
    # turn is_active to False instead
    "ALLOW_DELETE_ACCOUNT": False,
    # string path for email function wrapper, see the testproject example
    "EMAIL_ASYNC_TASK": False,
    # mutation error type
    "CUSTOM_ERROR_TYPE": None,
    # registration with no password
    "ALLOW_PASSWORDLESS_REGISTRATION": False,
    "SEND_PASSWORD_SET_EMAIL": False,

    "EMAIL_TEMPLATE_VARIABLES": {
        "frontend_domain": "the-frontend.com"
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# send email
if not DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.googlemail.com'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST_USER = config('EMAIL_ADRESS')
    EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')

AUTH_USER_MODEL = "users.CustomUser"
