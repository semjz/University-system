from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from management.models import Term

from utils.choices import COURSE_TYPES


class Course(models.Model):
    name = models.CharField(max_length=50)
    credits = models.FloatField(validators=(MinValueValidator(0),))
    type = models.CharField(choices=COURSE_TYPES, max_length=11)
    pre_requisites = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True
                                       , related_name="post_courses")
    co_requisites = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True
                                      , related_name="co_courses")
    schools = models.ManyToManyField(to="management.Faculty", related_name="courses")


class TermCourse(models.Model):
    class_date_time = models.DateTimeField()
    exam_date_time = models.DateTimeField()
    exam_site = models.CharField()
    capacity = models.PositiveIntegerField(validators=(MaxValueValidator(250),))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    professors = models.ManyToManyField("management.Professor")