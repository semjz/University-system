from rest_framework import serializers
from django.contrib.auth import get_user_model
from management.models import Student
from authentication.serializers import CreateUserSerializer, FullUpdateUserSerializer
import string
import secrets
from utils.choices import ENTRANCE_TERM_CHOICES

User = get_user_model()


def create_student_id(entrance_year, entrance_term):
    unique_id = ''.join(secrets.choice(string.digits) for _ in range(4))
    term = {ENTRANCE_TERM_CHOICES[0][0]: 1, ENTRANCE_TERM_CHOICES[1][0]: 2}
    return f"{entrance_year}{term[entrance_term]}{unique_id}"


class CreateStudentSerializer(serializers.ModelSerializer):
    user = CreateUserSerializer()

    class Meta:
        model = Student
        fields = ["user_id", "user", "major", "school", "entrance_year", "entrance_term"]
        read_only_fields = ("user_id",)

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["user_id"] = create_student_id(validated_data["entrance_year"]
                                                 , validated_data["entrance_term"])
        user = CreateUserSerializer().create(user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student


class RUDStudentSerializer(serializers.ModelSerializer):
    user = FullUpdateUserSerializer()

    class Meta:
        model = Student
        fields = ["user", "major", "school", "entrance_year", "entrance_term"]

    def update(self, instance, validated_data):
        if validated_data.get("user"):
            user_data = validated_data.pop("user")

            user_instance = instance.user
            for field, value in user_data.items():
                if field == "password":
                    instance.password = user_instance.set_password(value)
                else:
                    setattr(user_instance, field, value)

            user_instance.save()

        return super().update(instance, validated_data)
