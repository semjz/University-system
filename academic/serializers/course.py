from rest_framework import serializers

from academic.models import Course, TermCourse
from management.models import Term
from management.serializers.term import TermSerializer


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ("id",)


class TermCourseSerializer(serializers.ModelSerializer):
    queryset = TermCourse.objects.all()
    term = serializers.PrimaryKeyRelatedField(queryset=Term.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = TermCourse
        fields = ['class_date_time', 'exam_date_time', 'exam_site', 'capacity', 'course', 'term']

    # def validate(self, data):
    #     data['course.type']
