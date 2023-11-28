from django.contrib.auth import get_user_model

from rest_framework import serializers

from academic.models import Course
from authentication.serializers import FullUpdateUserSerializer, StudentUpdateUserSerializer
from management.serializers import RUDStudentSerializer


User = get_user_model()


class AssistantUpdateStudentSerializer(RUDStudentSerializer):
    user = FullUpdateUserSerializer()


class StudentUpdateStudentSerializer(AssistantUpdateStudentSerializer):
    user = StudentUpdateUserSerializer()


class StudentAllowedCoursesSerializer(serializers.Serializer):
    class Meta:
        model = Course
        fields = ("name", "credits", "type")

