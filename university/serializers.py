from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student
from authentication.serializers import CreateUserSerializer
import string
import secrets

User = get_user_model()


def create_student_id(entrance_year, entrance_term):
    unique_id = ''.join(secrets.choice(string.digits) for _ in range(4))
    term = {"Mehr": 1, "Bahman": 2}
    return f"{entrance_year}{term[entrance_term]}{unique_id}"


class CreatStudentSerializer(serializers.ModelSerializer):
    user = CreateUserSerializer()

    class Meta:
        model = Student
        fields = ["user", "major", "school", "entrance_year", "entrance_term"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["user_id"] = create_student_id(validated_data["entrance_year"]
                                                 , validated_data["entrance_term"])
        user = CreatUserSerializer().create(user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student
