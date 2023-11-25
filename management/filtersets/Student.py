from django_filters import rest_framework as filters
from management.models import Student
from utils.choices import MILITARY_STATUS_CHOICES


class StudentFilterSet(filters.FilterSet):
    first_name = filters.CharFilter(field_name="user__first_name", lookup_expr="icontains", label="First Name")
    last_name = filters.CharFilter(field_name="user__last_name", lookup_expr="icontains", label="Last Name")
    national_code = filters.NumberFilter(field_name="user__national_code", label="National Code")
    school = filters.CharFilter(field_name="school", lookup_expr="icontains", label="School")
    entrance_year = filters.NumberFilter(field_name="entrance_year", label="Entrance Year")
    military_status = filters.ChoiceFilter(choices=MILITARY_STATUS_CHOICES, field_name="military_status"
                                           , label="Military Status")
    major = filters.NumberFilter(field_name="major", lookup_expr="icontains", label="Major")

    class Meta:
        model = Student
        fields = ["school", "major", "entrance_year", "military_status"]
