from django.db import models

from academic.models import Course
from utils.choices import STAGE_CHOICES


class Faculty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Major(models.Model):
    school = models.ForeignKey(to=Faculty, on_delete=models.CASCADE, related_name="majors")
    name = models.CharField(max_length=128)
    units = models.IntegerField()
    stage = models.CharField(choices=STAGE_CHOICES, max_length=9)
    courses = models.ManyToManyField(to=Course, related_name='majors')

    def __str__(self):
        return self.name
