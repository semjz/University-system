from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg, Count
from utils.choices import *


User = get_user_model()


class ITManager(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id


class Student(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(to="Professor", on_delete=models.CASCADE, null=True, blank=True
                                   , related_name="student")
    major = models.ForeignKey(to="management.Major", on_delete=models.CASCADE, related_name="students")
    school = models.ForeignKey(to="management.Faculty", on_delete=models.CASCADE, related_name="students")
    entrance_year = models.IntegerField()
    entrance_term = models.CharField(choices=ENTRANCE_TERM_CHOICES, max_length=6)
    military_status = models.CharField(choices=MILITARY_STATUS_CHOICES, max_length=20)
    courses = models.ManyToManyField(to="academic.TermCourse", through="unitselection.Enrollment", blank=True)
    deleted_terms = models.ManyToManyField(to='Term', through='DeleteTerm', blank=True)
    max_term = models.IntegerField(default=12)


    @property
    def average_grade(self):
        average_grade = self.enrollments.get(student=self).aggregate(Avg("student_grade"))['student_grade__avg']
        return average_grade

    @property
    def sanavat(self):
        terms_count = self.terms.filter(student=self).aggregate(term_count=Count('name'))['term_count']
        return 12 - terms_count

    @property
    def passed_courses(self):
        passed_enrollments = self.enrollments.filter(course_condition=CourseCondition.PASSED)
        return [enrollment.course.course for enrollment in passed_enrollments]

    @property
    def current_courses(self):
        return self.enrollments.filter(course_condition=CourseCondition.IN_PROGRESS).course


class Professor(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    school = models.ForeignKey(to="management.Faculty", on_delete=models.CASCADE, related_name="professors")
    past_courses = models.ManyToManyField(to="academic.Course", blank=True)
    major = models.ForeignKey(to="management.Major", on_delete=models.CASCADE, related_name="professors")
    expertise = models.CharField(max_length=250, null=True, blank=True)
    rank = models.CharField(choices=PROFESSOR_RANK_CHOICES, max_length=20, null=True, blank=True)


class Assistant(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    school = models.OneToOneField(to="management.Faculty", on_delete=models.CASCADE)
    major = models.OneToOneField(to="management.Major", on_delete=models.CASCADE)



