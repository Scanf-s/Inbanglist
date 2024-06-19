from typing import List

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models import BooleanField, DateTimeField, EmailField


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
<<<<<<< HEAD
=======

>>>>>>> 05475956a48e8c6c5d0a2cb9e13625ce4b9b16ec
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
    email: EmailField = models.EmailField(max_length=30, unique=True, null=False)
    is_staff: BooleanField = models.BooleanField(default=False)
    is_active: BooleanField = models.BooleanField(default=True)

    # is_superuser는 PermissionsMixin에 이미 포함되어 있긴 함
    is_superuser: BooleanField = models.BooleanField(default=False)

    created_at: DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: DateTimeField = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
