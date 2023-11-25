from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg, Count

from utils.choices import *


User = get_user_model()


class ITManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id


class Student(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True, related_name="student")
    supervisor = models.ForeignKey(to="Professor", on_delete=models.CASCADE, null=True, blank=True
                                   , related_name="student")
    major = models.ForeignKey(to="management.Major", on_delete=models.CASCADE, related_name="students")
    school = models.ForeignKey(to="management.Faculty", on_delete=models.CASCADE, related_name="students")
    entrance_year = models.IntegerField()
    entrance_term = models.CharField(choices=ENTRANCE_TERM_CHOICES, max_length=6)
    military_status = models.CharField(choices=MILITARY_STATUS_CHOICES, max_length=20)
    courses = models.ManyToManyField(to="academic.Course", through="unitselection.Enrollment", blank=True)
    deleted_terms = models.ManyToManyField(to='Term', through='DeleteTerm', blank=True)

    @property
    def average_grade(self):
        enrollments = self.courses.get(student=self)
        average_grade = enrollments.aggregate(Avg("student_grade"))['student_grade__avg']
        return average_grade

    @property
    def sanavat(self):
        terms_count = self.terms.filter(student=self).aggregate(term_count=Count('id'))['term_count']
        return terms_count


class Professor(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True)
    school = models.ForeignKey(to="management.Faculty", on_delete=models.CASCADE, related_name="professors")
    past_courses = models.ManyToManyField(to="academic.Course", blank=True)
    major = models.ForeignKey(to="management.Major", on_delete=models.CASCADE, related_name="professors")
    expertise = models.CharField(max_length=250, null=True, blank=True)
    rank = models.CharField(choices=PROFESSOR_RANK_CHOICES, max_length=20, null=True, blank=True)


class Assistant(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True, related_name="assistant")
    school = models.OneToOneField(to="management.Faculty", on_delete=models.CASCADE)
    major = models.OneToOneField(to="management.Major", on_delete=models.CASCADE)
