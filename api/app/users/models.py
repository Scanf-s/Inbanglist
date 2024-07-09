import os

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models import BooleanField, CharField, EmailField

from common.models import TimeStampedModel
from common.platforms import OAuthPlatforms


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
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
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    email = models.EmailField(max_length=255, unique=True, null=False, db_index=True)
    username = models.CharField(max_length=255, null=True, db_index=True)
    profile_image = models.CharField(
        max_length=255, null=True, default=os.getenv("DEFAULT_PROFILE_IMAGE_URL")
    )  # aws s3 url
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class UserOAuth2Platform(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    oauth_platform = models.CharField(
        max_length=50,
        choices=OAuthPlatforms.platform_choices,
        default="none",
        null=True
    )
    oauth2_user_id = models.CharField(max_length=255, null=True)
