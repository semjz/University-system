import secrets
import string
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model

User = get_user_model()


def create_random_numeric_string(n):
    return ''.join(secrets.choice(string.digits) for _ in range(n))


class BaseUserFactory(DjangoModelFactory):
    class Meta:
        model = User
        exclude = ("phone_number1",)
        abstract = True

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    phone_number1 = factory.Faker("phone_number", locale="fa_IR")
    phone_number = factory.LazyAttribute(lambda o: o.phone_number1.replace(" ", "")[:13])
    gender = factory.Iterator(["male", "female"])
    password = factory.Faker('password')

    @factory.lazy_attribute
    def user_id(self):
        return create_random_numeric_string(4)

    @factory.lazy_attribute
    def national_code(self):
        return create_random_numeric_string(10)


class StudentUserFactory(BaseUserFactory):
    role = "Student"


class ProfessorUserFactory(BaseUserFactory):
    role = "Professor"


class AssistantUserFactory(BaseUserFactory):
    role = "Assistant"


class ItManagerUserFactory(BaseUserFactory):
    role = "IT Manager"
