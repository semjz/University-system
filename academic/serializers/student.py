from rest_framework import serializers
from django.contrib.auth import get_user_model
from management.models import Student
from authentication.serializers import UpdateUserByOthersSerializer
from management.serializers import RUDStudentSerializer

User = get_user_model()


class UpdateStudentSerializer(RUDStudentSerializer):
    user = UpdateUserByOthersSerializer()

    class Meta:
        model = Student
        fields = ["user", "major", "school", "entrance_year", "entrance_term"]
