# management/serializers/assistance.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from management.models import Assistant
from authentication.serializers import CreateUserSerializer, UpdateUserSerializer

User = get_user_model()

class AssistantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assistant
        fields = ["id", "user", "seniority", "faculty", "deputy_field"]

class AssistantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assistant
        fields = ["id", "user", "seniority", "faculty", "deputy_field"]

class CreateTeachingAssistantSerializer(serializers.ModelSerializer):
    user = CreateUserSerializer()

    class Meta:
        model = Assistant
        fields = ["user", "seniority", "faculty", "deputy_field"]


    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = CreateUserSerializer().create(user_data)
        assistant = Assistant.objects.create(user=user, **validated_data)
        return assistant


class UpdateTeachingAssistantSerializer(serializers.ModelSerializer):
    user = UpdateUserSerializer()

    class Meta:
        model = Assistant
        fields = ["user", "seniority", "faculty", "deputy_field"]

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

