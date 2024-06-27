# 이메일 전송을 처리하는 Celery 작업을 정의
import os

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


@shared_task
def send_activation_email_task(user_email: str, token: str) -> None:
    # activation_link = "http://127.0.0.1:8000" + reverse("user_email_activate", args=[token])
    activation_link = os.getenv("MAIN_DOMAIN") + reverse("user_email_activate", args=[token])
    subject = "Activate your account"
    body = f"""
    Hello,

    Please click the link below to activate your account.

    {activation_link}
    """
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user_email])
