from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student
from authentication.serializers import UserSerializer
import string
import secrets

User = get_user_model()


def create_student_id(entrance_year, entrance_term):
    unique_id = ''.join(secrets.choice(string.digits) for _ in range(4))
    term = {"Mehr": 1, "Bahman": 2}
    return f"{entrance_year}{term[entrance_term]}{unique_id}"


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ["user", "major", "school", "entrance_year", "entrance_term"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["user_id"] = create_student_id(validated_data["entrance_year"]
                                                 , validated_data["entrance_term"])
        user = CreateUserSerializer().create(user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        user_instance = instance.user
        for field, value in user_data.items():
            if field == "password":
                instance.password = user_instance.set_password(value)
            else:
                setattr(user_instance, field, value)

        user_instance.save()

        return instance
