from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "first_name", "last_name", "national_code", "phone_number"
                   , "email", "gender", "birth_date"]

    def validate_national_code(self, national_code):
        if not national_code.isnumeric():
            raise serializers.ValidationError("National code must only contain digits!")
        return national_code

    def validate_phone_number(self, phone_number):
        phone_number = phone_number.replace("+98", "0")
        if not phone_number.isnumeric():
            raise serializers.ValidationError("Phone number code must only contain digits!")
        return phone_number

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance


class CreateUserSerializer(UpdateUserSerializer):
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


class UpdateUserByOthersSerializer(UpdateUserSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "national_code", "phone_number", "email", "gender", "birth_date"]

