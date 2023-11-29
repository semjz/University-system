from rest_framework import serializers
from unitselection.models import Enrollment


class StudentCoursesReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = "__all__"
