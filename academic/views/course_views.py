from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from academic import filtersets
from academic.models import Course, TermCourse
from academic.permissions import IsCourseAssistant, IsTermCourseAssistant
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
    queryset = TermCourse.objects.all()
    serializer_class = TermCourseSerializer
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return (IsAuthenticated(),)
        else:
            return ((IsItManager | IsTermCourseAssistant)(),)

    http_method_names = ['get', 'post', 'put', 'patch', 'delete']



