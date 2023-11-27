import datetime

from rest_framework import serializers

from academic.models import Course, TermCourse
from management.models import Term


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

    def validate(self, data):
        now_time = datetime.datetime.now()
        if data["end_term_time"] > now_time > data["fix_course_end_time"]:
            raise serializers.ValidationError("Can't create a term course after Add/drop time end time "
                                              "until the end of current term")

