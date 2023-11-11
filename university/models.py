from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


COURSE_TYPES = [("general", "General"), ("specialized", "Specialized")
    , ("core", "Core"), ("optional", "Optional")]


class Course(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    credits = models.FloatField(blank=False, null=False, validators=(MinValueValidator(0),))
    type = models.CharField(choices=COURSE_TYPES, blank=False, null=False)
    pre_requisites = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True
                                       , related_name="post_courses")
    co_requisites = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True
                                      , related_name="co_courses")
    # schools = models.ManyToManyField(School)


class TermCourse(models.Model):
    class_date_time = models.DateTimeField(blank=False, null=False)
    exam_date_time = models.DateTimeField(blank=False, null=False)
    exam_site = models.CharField(blank=False, null=False)
    capacity = models.PositiveIntegerField(blank=False, null=False, validators=(MinValueValidator(250),))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    # term = models.ForeignKey(Term, on_delete=models.CASCADE, blank=True, null=True)
    # professors = models.ManyToManyField(Professor)

