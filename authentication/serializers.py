from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
import secrets
import string

User = get_user_model()


class CreatUserSerializer(serializers.ModelSerializer):
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
            raise serializers.ValidationError("Passwords don't match!")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(
            **validated_data
        )
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_pass = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_new_pass = serializers.CharField(write_only=True, required=True)
    old_pass = serializers.CharField(write_only=True, required=True)
    reset_token = serializers.CharField(write_only=True, max_length=50)

    class Meta:
        model = User
        fields = ["old_pass", "new_pass", "confirm_new_pass", "reset_token"]

    def validate_old_pass(self, password):
        user = self.context['request'].user
        if not user.check_password(password):
            raise serializers.ValidationError("Old password is not correct!")
        return password

    def validate_reset_token(self, reset_token):
        user = self.context['request'].user
        if not cache.get(user.user_id):
            raise serializers.ValidationError("No password reset request submitted for this user")
        if not str(cache.get(user.user_id)) == reset_token:
            raise serializers.ValidationError("Reset token is not correct!")

    def validate(self, data):
        if data['new_pass'] != data['confirm_new_pass']:
            raise serializers.ValidationError("Passwords don't match!")

        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_pass'])
        instance.save()
        return instance

