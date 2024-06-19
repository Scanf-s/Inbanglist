from .settings import *
# CI 환경을 위한 별도의 설정 파일
DEBUG = False
ALLOWED_HOSTS = ["localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get('RDS_DB_NAME'),
        "USER": os.environ.get('RDS_USER'),
        "PASSWORD": os.environ.get('RDS_PASSWORD'),
        "HOST": os.environ.get('RDS_HOST'),
        "PORT": os.environ.get('RDS_PORT'),
    }
}