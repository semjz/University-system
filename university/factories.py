import factory
from factory.django import DjangoModelFactory

from .choices import *
from .models import Student, School, Major, Course
from authentication.factories import StudentUserFactory


class SchoolFactory(DjangoModelFactory):
    class Meta:
        model = School

    name = factory.Faker("name")


class MajorFactory(DjangoModelFactory):
    class Meta:
        model = Major

    name = factory.Faker("name")
    units = 100
    stage = factory.Iterator([choice[0] for choice in STAGE_CHOICES])
    school = factory.SubFactory(SchoolFactory)


class StudentFactory(DjangoModelFactory):
    class Meta:
        model = Student

    user = factory.SubFactory(StudentUserFactory, student=None)
    school = factory.SubFactory(SchoolFactory)
    major = factory.SubFactory(MajorFactory, school=factory.SelfAttribute('..school'))
    entrance_year = factory.Faker("year")
    entrance_term = factory.Iterator([choice[0] for choice in ENTRANCE_TERM_CHOICES])
    military_status = factory.Iterator([choice[0] for choice in MILITARY_STATUS_CHOICES])


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = Course

    name = factory.Faker("name")
    credits = factory.Iterator([i for i in range(10)])
    type = factory.Iterator([choice[0] for choice in COURSE_TYPES])

    @factory.post_generation
    def schools(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.schools.add(*extracted)


