from rest_framework import serializers
from django.contrib.auth import get_user_model
from utils.choices import ENTRANCE_TERM_CHOICES
from management.models import Term

User = get_user_model()


class TermSerializer(serializers.ModelSerializer):
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