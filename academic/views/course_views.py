from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from academic import filtersets
from academic.models import Course
from academic.permissions import IsCourseAssistant
from academic.serializers import CourseSerializer
from academic.serializers.course import TermCourseSerializer

from management.permissions import IsItManager


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    http_method_names = ("get", "post", "put", "patch", "delete")
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = filtersets.CourseFilterSet
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return (IsAuthenticated(),)
        else:
            return ((IsItManager | IsCourseAssistant)(),)


class TermCourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = TermCourseSerializer
    permission_classes = [IsItManager | IsCourseAssistant]
    pagination_class = PageNumberPagination

    http_method_names = ['get', 'post', 'put', 'patch', 'delete']



