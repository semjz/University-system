from datetime import datetime

import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from . import models
from management.factories import ProfessorFactory
from utils.choices import COURSE_TYPES


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

    @factory.post_generation
    def pre_requisites(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.pre_requisites.add(*extracted)

    @factory.post_generation
    def co_requisites(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.co_requisites.add(*extracted)


class TermCourseFactory(DjangoModelFactory):

    class Meta:
        model = models.TermCourse

    class_date_time = factory.LazyFunction(datetime.now)
    exam_site = factory.fuzzy.FuzzyText(length=5)
    capacity = factory.Iterator([i for i in range(100)])
    course = factory.SubFactory(CourseFactory)
    professor = factory.SubFactory(ProfessorFactory)

