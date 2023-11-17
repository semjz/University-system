from django_filters import rest_framework as filters
from .models import Student


class StudentFilterSet(filters.FilterSet):
    first_name = filters.CharFilter(field_name="user__first_name", label="First Name")
    last_name = filters.CharFilter(field_name="user__last_name", label="Last Name")
    national_code = filters.NumberFilter(field_name="user__national_code", label="National Code")
    school = filters.NumberFilter(field_name="school", label="School")
    entrance_year = filters.NumberFilter(field_name="entrance_year", label="Entrance Year")
    military_status = filters.NumberFilter(field_name="military_status", label="Military Status")
    major = filters.NumberFilter(field_name="major", label="Major")

    class Meta:
        model = Student
        fields = ["school", "major", "entrance_year", "military_status"]