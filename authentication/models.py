import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from .managers import CustomUserManger


# Create your models here.
class User(AbstractUser):
    GENDERS_CHOICES = [("male", "male"), ("female", "female")]
    ROLES_CHOICES = [("Student", "Student"), ("Professor", "Professor"), ("Assistant", "Assistant")
                     , ("It-manager", "It-manager")]

    username = models.CharField(max_length=8, validators=[MinLengthValidator(4)], unique=True
                                , blank=True, null=True)
    profile_image = models.ImageField("user_image")
    phone_number = models.CharField(max_length=11, validators=[MinLengthValidator(11)], unique=True)
    national_code = models.CharField(max_length=10, validators=[MinLengthValidator(10)], unique=True)
    gender = models.CharField(choices=GENDERS_CHOICES)
    role = models.CharField(choices=ROLES_CHOICES, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    objects = CustomUserManger()

    REQUIRED_FIELDS = ["email", "national_code", "phone_number", "role"]

    def __str__(self):
        return str(self.username)

