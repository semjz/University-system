from django_filters import rest_framework as filters
from utils.choices import PROFESSOR_RANK_CHOICES


class ProfessorFilter(filters.FilterSet):
    first_name = filters.CharFilter(field_name='user__first_name', lookup_expr='icontains', label='First Name')
    last_name = filters.CharFilter(field_name='user__last_name', lookup_expr='icontains', label='Last Name')
    user_id = filters.CharFilter(field_name='user__user_id', lookup_expr='icontains', label='User Id')
    national_code = filters.CharFilter(field_name='user__national_code', lookup_expr='icontains', label='National Code')
    school = filters.CharFilter(field_name='school__name', lookup_expr='icontains', label='School Name')
    major = filters.CharFilter(field_name='major__name', lookup_expr='icontains', label='Major Name')
    rank = filters.CharFilter(choices=PROFESSOR_RANK_CHOICES, field_name='rank', lookup_expr='exact', label='Rank')
