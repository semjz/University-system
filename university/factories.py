import factory
from factory.django import DjangoModelFactory

import university.models as models
from .choices import *
from authentication.factories import StudentUserFactory, AssistantUserFactory, ItManagerUserFactory, \
    ProfessorUserFactory


class SchoolFactory(DjangoModelFactory):
    class Meta:
        model = models.School

    name = factory.Faker("name")


class MajorFactory(DjangoModelFactory):
    class Meta:
        model = models.Major

    name = factory.Faker("name")
    units = 100
    stage = factory.Iterator([choice[0] for choice in STAGE_CHOICES])
    school = factory.SubFactory(SchoolFactory)


class StudentFactory(DjangoModelFactory):
    class Meta:
        model = models.Student

    user = factory.SubFactory(StudentUserFactory, student=None)
    school = factory.SubFactory(SchoolFactory)
    major = factory.SubFactory(MajorFactory, school=factory.SelfAttribute('..school'))
    entrance_year = factory.Faker("year")
    entrance_term = factory.Iterator([choice[0] for choice in ENTRANCE_TERM_CHOICES])
    military_status = factory.Iterator([choice[0] for choice in MILITARY_STATUS_CHOICES])


class AssistantFactory(DjangoModelFactory):
    class Meta:
        model = models.Assistant

    user = factory.SubFactory(AssistantUserFactory, assistant=None)
    school = factory.SubFactory(SchoolFactory)
    major = factory.SubFactory(MajorFactory)


class ITManagerFactory(DjangoModelFactory):
    class Meta:
        model = models.ITManager

    user = factory.SubFactory(ItManagerUserFactory)


class ProfessorFactory(DjangoModelFactory):
    class Meta:
        model = models.Professor

    user = factory.SubFactory(ProfessorUserFactory)
    school = factory.SubFactory(SchoolFactory)
    major = factory.SubFactory(MajorFactory)


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = models.Course

    name = factory.Faker("name")
    credits = factory.Iterator([i for i in range(10)])
    type = factory.Iterator([choice[0] for choice in COURSE_TYPES])

    @factory.post_generation
    def schools(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.schools.add(*extracted)
