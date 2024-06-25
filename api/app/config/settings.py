"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os  # os와 상호작용을 위해 사용
from datetime import timedelta  # 시간 간격 표현 모듈
from pathlib import Path  # 파일 경로 다루는 모듈

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent  # 프로젝트 루트 디렉토리

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Django 프로젝트의 비밀 키. 환경 변수로부터 가져오며 이 파일이 존재하지 않는다면 기본값으로 제공함
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-1@h*pw1qi%gop_5-hn(cpsdy*b4q^gd)s+o9h39z6ky$0h@zyg",
)

# SECURITY WARNING: don't run with debug turned on in production!
# 디버그 모드. 환경 변수로부터 불러와서 설정하게 된다.
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

# Django 백엔드 서버에 접속할 수 있는 목록. 환경변수에서 가져와서 설정한다.
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")

# Application definition

DJANGO_SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

CUSTOM_USER_APPS = [
    "common.apps.CommonConfig",  # common app
    "afreecatv.apps.AfreecatvConfig",  # AfreecaTV app
    "youtube.apps.YoutubeConfig",  # YouTube app
    "chzzk.apps.ChzzkConfig",  # Chzzk app
    "users.apps.UsersConfig",  # Users app
    "core.apps.CoreConfig",  # Core app
]

LIBRARIES = [
    "corsheaders",  # Django-CORS-Headers
    "drf_spectacular",  # DRF-Spectacular
    "django_extensions",  # Django-Extensions
    "rest_framework",  # DRF
    "rest_framework.authtoken",  # DRF Auth
    "rest_framework_simplejwt.token_blacklist",
]

INSTALLED_APPS = DJANGO_SYSTEM_APPS + CUSTOM_USER_APPS + LIBRARIES

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",  # 기본 스키마 클래스 설정.
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # 기본 인증 클래스 설정.
    ),
}

# 요청과 응답을 처리하는 미들웨어 목록
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # CORS 미들웨어 추가
]

"""
**CORS(Cross-Origin Resource Sharing)**는 
웹 브라우저가 다른 출처(도메인, 프로토콜, 포트)에 있는 리소스에 접근하는 것을 제한하는 보안 기능입니다. 
예를 들어, 프론트엔드 애플리케이션이 http://localhost:3000에서 실행되고, 
백엔드 API가 http://localhost:8000에서 실행된다면, 
이는 서로 다른 출처로 간주되어 브라우저는 기본적으로 이러한 요청을 차단합니다.

django-cors-headers 패키지는 Django 애플리케이션에서 CORS 설정을 쉽게 할 수 있게 도와줍니다. 
이 패키지를 사용하여 특정 출처에서 오는 요청을 허용하거나 거부할 수 있습니다.
"""
# CORS 설정 (필요에 따라 도메인 추가)
# 사용할 HTTP Method 옵션
CORS_ALLOW_METHODS = [
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# 허용할 HTTP Header
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://inbanglist.com",
    "http://www.inbanglist.com",
    "http://localhost:8000",
    "http://localhost:5173",
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://\w+\.inbanglist\.com$",
]

CORS_ALLOW_ALL_ORIGINS = False

# 프로젝트의 루트 URL 설정 파일
ROOT_URLCONF = "config.urls"

# 사용자에게 보여줄 웹페이지 설정 (관리자 페이지가 아닌 프론트엔드 페이지를 사용 예정이라 사용하지 않을 수도 있음)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

# WebServer Gateway Interface 애플리케이션 경로
WSGI_APPLICATION = "config.wsgi.application"

# Django에서 사용하는 Default Database 설정
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Favicon 설정
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Auth User Model 설정 (해당 Model를 사용해서 Auth 관련 작업을 수행한다)
AUTH_USER_MODEL = "users.User"

# Simple JWT Token Configurations
# SIMPLE JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=3),
    "SIGNING_KEY": "SECRET",
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
}

# DRF-SPECTACULAR
SPECTACULAR_SETTINGS = {
    "TITLE": "API 문서",
    "DESCRIPTION": "API for AfreecaTV, Chzzk, and Youtube",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "TAGS": [
        {"name": "User", "description": "User 관련 API"},
        {"name": "AfreecaTV", "description": "아프리카TV API"},
        {"name": "Chzzk", "description": "치지직 API"},
        {"name": "Youtube", "description": "유튜브 라이브 API"},
    ],
}
