from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models import BooleanField, CharField, EmailField

from common.models import TimeStampedModel
from common.platforms import OAuthPlatforms


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """
        Creates a new user with the given email and password. If the email is not provided, a ValueError will be raised.

        Args:
            email (str): The email address of the user.
            password (str, optional): The password for the user. Defaults to None.
            **extra_fields: Additional fields to be passed to the User model.

        Returns:
            User
        """
        if not email:
            raise ValueError("The Email field must be set")

        if not password:
            raise ValueError("The Password field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_social_user(self, email, oauth_platform, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, oauth_platform=oauth_platform)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    email: EmailField = models.EmailField(max_length=255, unique=True, null=False)
    username: CharField = models.CharField(max_length=255, null=True)
    is_staff: BooleanField = models.BooleanField(default=False)
    is_active: BooleanField = models.BooleanField(default=False)
    oauth_platform: CharField = models.CharField(
        max_length=50, choices=OAuthPlatforms.platform_choices, default="none", null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class NaverUserId(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    naver_user_id = models.CharField(max_length=255, null=True)


class GoogleUserId(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    google_user_id = models.CharField(max_length=255, null=True)
