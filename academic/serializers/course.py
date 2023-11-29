import datetime

from rest_framework import serializers

from academic.models import Course, TermCourse
from management.models import Term, Faculty


class CourseSerializer(serializers.ModelSerializer):

    pre_requisites = serializers.SlugRelatedField(queryset=Course.objects.all(), slug_field="name", many=True
                                                  , required=False)
    co_requisites = serializers.SlugRelatedField(queryset=Course.objects.all(), slug_field="name", many=True
                                                 , required=False)
    schools = serializers.SlugRelatedField(queryset=Faculty.objects.all(), slug_field="name", many=True
                                           , required=False)

    class Meta:
        model = Course
        exclude = ("id",)


class CourseReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ("id", "schools")


class TermCourseSerializer(serializers.ModelSerializer):
    queryset = TermCourse.objects.all()
    term = serializers.SlugRelatedField(queryset=Term.objects.all(), slug_field="name")
    course = serializers.SlugRelatedField(queryset=Course.objects.all(), slug_field="name")

    class Meta:
        model = TermCourse
        fields = ['class_date_time', 'exam_date_time', 'exam_site', 'capacity', 'course', 'term']

    def validate(self, data):
        now_time = datetime.datetime.now()
        if data["end_term_time"] > now_time > data["fix_course_end_time"]:
            raise serializers.ValidationError("Can't create a term course after Add/drop time end time "
                                              "until the end of current term")



