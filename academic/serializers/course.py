from rest_framework import serializers

from academic.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ("id",)
