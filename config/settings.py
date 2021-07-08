"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "t%_hh9z6u%cyjkzftdse87t-e*_$r9y69j6mzdo-)uuev%9=qr"

# SECURITY WARNING: don't run with debug turned on in production!
# 개발 단계에서 켜두는 것. 에러시 웹에서 에러 페이지를 보여준다. 끄면 404

# DEBUG = bool(os.environ.get("DEBUG"))
DEBUG = True

ALLOWED_HOSTS = [".elasticbeanstalk.com", "127.0.0.1"]


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "django_countries",
    "django_seed",
    "storages",
]

PROJECT_APPS = [
    "core.apps.CoreConfig",
    "users.apps.UsersConfig",
    "rooms.apps.RoomsConfig",
    "reviews.apps.ReviewsConfig",
    "reservations.apps.ReservationsConfig",
    "lists.apps.ListsConfig",
    "conversations.apps.ConversationsConfig",
]


INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
if not DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": os.environ.get("RDS_HOST"),
            "NAME": os.environ.get("RDS_NAME"),
            "USER": os.environ.get("RDS_USER"),
            "PASSWORD": os.environ.get("RDS_PASSWORD"),
            "PORT": "5432",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"  # 이건 URL. 폴더명이랑 관련 없음

STATIC_ROOT = STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]  # 이건 접근할 수 있는 폴더 지정

AUTH_USER_MODEL = "users.User"

# 미디어 파일 저장 경로를 설정
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")

MEDIA_URL = "/media/"  # 이건 경로라기 보다는 Url 에 입력되는 키워드에 가까움.
# media 앞에 / 를 사용하면 절대 경로가 지정된다.
# urls 에 추가해 줘야함.

# Email Configuration

EMAIL_HOST = "smtp.mailgun.org"
EMAIL_PORT = "587"
EMAIL_HOST_USER = os.environ.get("MAILGUN_USERNAME")
EMAIL_HOST_PASSWORD = os.environ.get("MAILGUN_PASSWORD")
EMAIL_FROM = "HANUM@sandboxb8bf853cc29f4cc3bf4b1d4ebbd0e59e.mailgun.org"


# for login required decorator (Photo Delete function)

LOGIN_URL = "/users/login"

# Locale

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

# Language

LANGUAGE_COOKIE_NAME = "django_language"

# if not DEBUG:

# DEFAULT_FILE_STORAGE = "config.custom_storages.UploadStorage"
# STATICFILES_STORAGE = "config.custom_storages.StaticStorage"
# AWS_ACCESS_KEY_ID = "AKIAV2LIRUS26YEFO5HP"
# AWS_SECRET_ACCESS_KEY = "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"
# AWS_STORAGE_BUCKET_NAME = "beerb-2"
# AWS_DEFAULT_ACL = "public-read"
# AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
# AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com"
# STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"

DEFAULT_FILE_STORAGE = "config.custom_storages.UploadStorage"
STATICFILES_STORAGE = "config.custom_storages.StaticStorage"
AWS_ACCESS_KEY_ID = os.environ.get("IAM_KEY")
AWS_SECRET_ACCESS_KEY = os.environ.get("IAM_PASSWORD")
AWS_STORAGE_BUCKET_NAME = "beerb-clone"
AWS_DEFAULT_ACL = "public-read"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
