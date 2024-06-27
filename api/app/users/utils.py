from typing import Union, cast, Dict

from django.conf import settings
from itsdangerous import URLSafeSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


def generate_email_token(user_email: str) -> str:
    """
    Generates an email verification token for the given user.
    """
    serializer = URLSafeSerializer(settings.SECRET_KEY)  # USE Django settings SECRET_KEY
    return serializer.dumps(user_email, salt=settings.SECRET_KEY)


def confirm_email_token(token, expiration=3600) -> Union[str, bool]:
    """
    Verifies an email verification token.
    """
    serializer = URLSafeSerializer(settings.SECRET_KEY)
    try:
        email: str = serializer.loads(token, salt=settings.SECRET_KEY, max_age=expiration)
    except:
        return False
    return email


def get_jwt_tokens_for_user(user: User) -> Dict[str, str]:
    refresh: RefreshToken = cast(RefreshToken, RefreshToken.for_user(user))
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
