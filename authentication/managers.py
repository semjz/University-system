from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password
from rolepermissions.roles import assign_role


class CustomUserManger(UserManager):
    def create_user(self, user_id, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        is_staff = extra_fields.get("is_staff")
        email = self.normalize_email(email)
        role = extra_fields.get("role")
        if not role:
            raise ValueError("The user role must be set")
        user = self.model(user_id=user_id, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        if not is_staff:
            assign_role(user, role)
        return user

    def create_superuser(self, user_id, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "Super Admin")
        self.create_user(user_id, email, password, **extra_fields)

    def create(self, **kwargs):
        return self.create_user(**kwargs)
