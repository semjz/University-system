from rest_framework import serializers
from django.contrib.auth import get_user_model
from .choices import ENTRANCE_TERM_CHOICES
from .models import Student, Term, Course, Professor
from authentication.serializers import CreateUserSerializer
import string
import secrets

User = get_user_model()


def create_student_id(entrance_year, entrance_term):
    unique_id = ''.join(secrets.choice(string.digits) for _ in range(4))
    term = {"Mehr": 1, "Bahman": 2}
    return f"{entrance_year}{term[entrance_term]}{unique_id}"


def create_professor_id():
    unique_id = ''.join(secrets.choice(string.digits) for _ in range(6))
    return unique_id


class CreateStudentSerializer(serializers.ModelSerializer):
    user = CreateUserSerializer()

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


class AdminTermSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(write_only=True)
    term_type = serializers.ChoiceField(choices=ENTRANCE_TERM_CHOICES, write_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Term
        fields = '__all__'

    def validate_year(self, year):
        if year >= 1370:
            return year

    def create(self, validated_data):
        name = validated_data.get('term_type') + str(validated_data.get('year'))
        validated_data.pop('year')
        validated_data.pop('term_type')
        validated_data['name'] = name
        return super().create(validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get('term_type') + str(validated_data.get('year'))
        validated_data.pop('year')
        validated_data.pop('term_type')
        validated_data['name'] = name
        return super().update(instance, validated_data)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class AdminProfessorSerializer(serializers.ModelSerializer):
    user = CreateUserSerializer()

    class Meta:
        model = Professor
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["user_id"] = create_professor_id()
        user = CreateUserSerializer().create(user_data)
        validated_data['user'] = user
        return super().create(validated_data)
