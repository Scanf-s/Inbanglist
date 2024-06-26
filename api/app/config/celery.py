from __future__ import absolute_import, unicode_literals

# __future__ : Python 2.7, 3.x compatibility check
# absolute_import : Python 3.x import check
# unicode_literals : Process all Unicode characters in string
import os

from celery import Celery

# To create Celery instance

# Django의 settings 모듈을 Celery의 기본 설정 모듈로 사용하도록 지정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("live_streaming_list")

# Get celery settings from django.conf:settings (settings.py)
app.config_from_object("django.conf:settings", namespace="CELERY")

# Django의 모든 등록된 task 모듈을 로드합니다.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
