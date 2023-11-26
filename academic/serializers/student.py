from django.contrib.auth import get_user_model

from management.models import Student
from authentication.serializers import FullUpdateUserSerializer, StudentUpdateUserSerializer
from management.serializers import RUDStudentSerializer


User = get_user_model()


class AssistantUpdateStudentSerializer(RUDStudentSerializer):
    user = FullUpdateUserSerializer()


class StudentUpdateStudentSerializer(AssistantUpdateStudentSerializer):
    user = StudentUpdateUserSerializer()

