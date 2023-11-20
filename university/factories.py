import factory
import random
from factory import Faker
from factory.django import DjangoModelFactory

from .choices import *
from .models import Student, School, Major
from authentication.factories import StudentUserFactory


class SchoolFactory(DjangoModelFactory):
    class Meta:
        model = School

    name = Faker("name")


class MajorFactory(DjangoModelFactory):
    class Meta:
        model = Major

    name = Faker("name")
    units = 100
    stage = random.choice(STAGE_CHOICES)[0]
    school = factory.SubFactory(SchoolFactory)


class StudentFactory(DjangoModelFactory):
    class Meta:
        model = Student

    user = factory.SubFactory(StudentUserFactory, student=None)
    school = factory.SubFactory(SchoolFactory)
    major = factory.SubFactory(MajorFactory, school=factory.SelfAttribute('..school'))
    entrance_year = Faker("year")
    entrance_term = random.choice(ENTRANCE_TERM_CHOICES)[0]
    military_status = random.choice(MILITARY_STATUS_CHOICES)[0]


