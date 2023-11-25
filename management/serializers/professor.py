from rest_framework import serializers
from django.contrib.auth import get_user_model
from management.models.members import Professor
from authentication.serializers import CreateUserSerializer
import string
import secrets

User = get_user_model()


def create_professor_id():
    unique_id = ''.join(secrets.choice(string.digits) for _ in range(6))
    return unique_id


class ProfessorSerializer(serializers.ModelSerializer):
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

