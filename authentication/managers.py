from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as g
from django.contrib.auth.hashers import make_password

import secrets
import string


class CustomUserManger(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        email = self.normalize_email(email)
        role = extra_fields.get("role")
        is_staff = extra_fields.get("is_staff")
        if not role and not is_staff:
            raise ValueError("The user role must be set")
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "It-manager")
        username = ''.join(secrets.choice(string.digits) for _ in range(4))

        if extra_fields.get("is_staff") is not True:
            raise ValueError(g("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(g("Superuser must have is_superuser=True."))
        self.create_user(username, email, password, **extra_fields)
        print(f"user id: {username}")
