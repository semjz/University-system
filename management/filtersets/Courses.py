from django_filters import rest_framework as filters
from academic.models import Course


class CourseFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains", label="Name")
    schools = filters.CharFilter(field_name="schools__name", lookup_expr="icontains", label="Faculty Name")

    class Meta:
        model = Course
        fields = ["name", "schools"]
        