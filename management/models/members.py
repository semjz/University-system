from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Avg, Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

from authentication.roles import AssistantRole
from management.mixins import UserIdPermissionMixin
from utils.choices import *


User = get_user_model()


class ITManager(UserIdPermissionMixin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
        terms_count = self.terms.filter(student=self).aggregate(term_count=Count('name'))['term_count']
        return terms_count


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(to="management.Faculty", on_delete=models.CASCADE, related_name="professors")
    past_courses = models.ManyToManyField(to="academic.Course", blank=True)
    major = models.ForeignKey(to="management.Major", on_delete=models.CASCADE, related_name="professors")
    expertise = models.CharField(max_length=250, null=True, blank=True)
    rank = models.CharField(choices=PROFESSOR_RANK_CHOICES, max_length=20, null=True, blank=True)


class Assistant(UserIdPermissionMixin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.OneToOneField(to="management.Faculty", on_delete=models.CASCADE)
    major = models.OneToOneField(to="management.Major", on_delete=models.CASCADE)


@receiver(post_save, sender=Assistant)
def user_post_save(sender, **kwargs):
    """
    Create a Profile instance for all newly created User instances. We only
    run on user creation to avoid having to check for existence on each call
    to User.save.
    """
    assistant, created = kwargs["instance"], kwargs["created"]
    if created and assistant.user_id != settings.ANONYMOUS_USER_NAME:
        assign_perm("management.can_modify_user_id", assistant.user)
