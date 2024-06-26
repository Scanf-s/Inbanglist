from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models import BooleanField, DateTimeField, EmailField


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

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email: EmailField = models.EmailField(max_length=255, unique=True, null=False)
    is_staff: BooleanField = models.BooleanField(default=False)
    is_active: BooleanField = models.BooleanField(default=False)

    created_at: DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: DateTimeField = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
