from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache

User = get_user_model()


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


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=200)