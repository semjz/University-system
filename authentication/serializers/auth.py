from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


User = get_user_model()


class ChangePasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ChangePasswordActionSerializer(serializers.Serializer):
    reset_token = serializers.CharField(max_length=50, required=True)
    new_pass = serializers.CharField(required=True, validators=[validate_password])
    confirm_new_pass = serializers.CharField(required=True)

    def validate_reset_token(self, reset_token):
        if not reset_token:
            serializers.ValidationError("A reset token must be provided!")
        return reset_token

    def validate(self, data):
        if data['new_pass'] != data['confirm_new_pass']:
            raise serializers.ValidationError("Passwords don't match!")

        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=200)
