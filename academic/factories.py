import factory
from factory.django import DjangoModelFactory

from . import models
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
