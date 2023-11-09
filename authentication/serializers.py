from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
import secrets
import string

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=128, required=True, write_only=True)

    class Meta:
        model = User
        fields = ["user_id", "first_name", "last_name", "national_code", "phone_number", "email"
                  , "role", "gender", "birth_date", "password", "confirm_password"]
        read_only_fields = ["user_id"]

    def validate_password(self, password):
        validate_password(password)
        return password

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        validated_data["user_id"] = ''.join(secrets.choice(string.digits) for _ in range(4))
        user = User.objects.create_user(
            **validated_data
        )
        return user
