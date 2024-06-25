from itsdangerous import URLSafeSerializer
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail

def generate_email_token(user_email: str) -> str:
    """
    Generates an email verification token for the given user.
    """
    serializer = URLSafeSerializer(settings.SECRET_KEY) # USE Django settings SECRET_KEY
    return serializer.dumps(user_email, salt=settings.SECRET_KEY)

def confirm_email_token(token, expiration=3600) -> str | bool:
    """
    Verifies an email verification token.
    """
    serializer = URLSafeSerializer(settings.SECRET_KEY)
    try:
        email: str = serializer.loads(token, salt=settings.SECRET_KEY, max_age=expiration)
    except:
        return False
    return email

def send_activation_email(user_email: str, token) -> None:
    activation_link = "http://127.0.0.1:8000" + reverse('user_email_activate', args=[token])
    subject: str = "Activate your account"
    body: str = f"""
    Hello,

    Please click the link below to activate your account.

    {activation_link}
    """
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user_email])
