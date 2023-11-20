from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from .managers import CustomUserManger
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    GENDERS_CHOICES = [("male", "male"), ("female", "female")]
    ROLES_CHOICES = [("student", "Student"), ("professor", "Professor"), ("assistant", "Assistant")
        , ("it-manager", "It-manager")]

    username = None
    user_id = models.CharField(max_length=8, validators=[MinLengthValidator(4)], unique=True
                               , blank=True, null=True)

    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150, unique=True)
    email = models.EmailField(_("email address"))

    profile_image = models.ImageField("user_image")
    phone_number = models.CharField(_("phone number"), max_length=13, validators=[MinLengthValidator(11)]
                                    , unique=True)
    national_code = models.CharField(_("national code"), max_length=10, validators=[MinLengthValidator(10)]
                                     , unique=True)
    gender = models.CharField(choices=GENDERS_CHOICES, max_length=10)
    role = models.CharField(_("role"), choices=ROLES_CHOICES,  max_length=20)
    birth_date = models.DateField(null=True, blank=True)

    objects = CustomUserManger()

    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = ["email", "first_name", "last_name", "national_code", "phone_number", "role"]

    def __str__(self):
        return str(self.username)

class Assistant(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    employee_number = models.CharField(max_length=20, unique=True)
    national_code = models.CharField(max_length=20, unique=True)
    faculty = models.CharField(max_length=255)
    field = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
