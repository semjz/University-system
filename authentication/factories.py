import secrets
import string
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model

User = get_user_model()


def create_random_national_code():
    return ''.join(secrets.choice(string.digits) for _ in range(10))


def create_random_user_id():
    return ''.join(secrets.choice(string.digits) for _ in range(4))


def coerce_phone_number(obj):
    return obj.phone_number1.replace(" ", "")[:13]


class BaseUserFactory(DjangoModelFactory):
    class Meta:
        model = User
        exclude = ("phone_number1",)
        abstract = True

    user_id = factory.LazyFunction(create_random_user_id)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    phone_number1 = factory.Faker("phone_number", locale="fa_IR")
    phone_number = factory.LazyAttribute(coerce_phone_number)
    national_code = factory.LazyFunction(create_random_national_code)
    gender = factory.Iterator(["male", "female"])
    password = factory.Faker('password')


class StudentUserFactory(BaseUserFactory):
    role = "Student"


class ProfessorUserFactory(BaseUserFactory):
    role = "Professor"


class AssistantUserFactory(BaseUserFactory):
    role = "Assistant"


class ItManagerUserFactory(BaseUserFactory):
    role = "IT Manager"
