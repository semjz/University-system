from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from . import filtersets
from .models import Student
from .permissions import IsItManager
from .serializers import UpdateStudentSerializer, CreateStudentSerializer, CourseSerializer


class ITManagerStudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    permission_classes = (IsAuthenticated, IsItManager)
    http_method_names = ("get", "post", "put", "patch", "delete")
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = filtersets.StudentFilterSet

    def perform_destroy(self, instance):
        instance.user.delete()

    def get_serializer_class(self):
        if self.action == "partial_update" or self.action == "update":
            return UpdateStudentSerializer
        else:
            return CreateStudentSerializer
