from django.contrib.auth import get_user_model

from rest_framework import serializers

from academic.models import Course
from authentication.serializers import FullUpdateUserSerializer, RestrictUpdateUserSerializer
from management.serializers import RUDStudentSerializer


User = get_user_model()


class AssistantUpdateStudentSerializer(RUDStudentSerializer):
    user = FullUpdateUserSerializer()


class StudentUpdateStudentSerializer(RUDStudentSerializer):
    user = RestrictUpdateUserSerializer()


class StudentAllowedCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("name", "credits", "type")

