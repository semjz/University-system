from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from academic import filtersets
from academic.models import Course
from academic.permissions import IsITManagerOrIsCourseAssistant
from academic.serializers import CourseSerializer


# Create your views here.

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
            return (IsITManagerOrIsCourseAssistant(),)