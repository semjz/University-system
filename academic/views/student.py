from django_filters import rest_framework as filters
from rest_framework import mixins

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from academic.permissions import IsAssistant, IsStudent
from management.models import Student
from management.filtersets import StudentFilterSet
from management.serializers import RUDStudentSerializer
from academic.serializers import UpdateStudentSerializer


class StudentListRetrieveSet(GenericViewSet
                             , mixins.ListModelMixin
                             , mixins.RetrieveModelMixin
                             , mixins.UpdateModelMixin):
    queryset = Student.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StudentFilterSet

    def get_permissions(self):
        if self.action in ["retrieve", "list"]:
            return IsAuthenticated(), IsAssistant()
        else:
            return IsAuthenticated(), IsStudent()

    def get_serializer_class(self):
        if self.action in ["retrieve", "list"]:
            return RUDStudentSerializer
        else:
            return UpdateStudentSerializer

