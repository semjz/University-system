from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from . import filtersets
from .filtersets.professor import ProfessorFilter
from .models import Student, Term, Professor, Faculty
from .permissions import IsItManager
from .serializers import RUDStudentSerializer, CreateStudentSerializer, FacultySerializer
from .serializers.professor import ProfessorSerializer
from .serializers.term import TermSerializer


class ITManagerStudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    permission_classes = (IsAuthenticated, IsItManager)
    http_method_names = ("get", "post", "put", "patch", "delete")
    pagination_class = PageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = filtersets.StudentFilterSet

    def perform_destroy(self, instance):
        instance.user.delete()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateStudentSerializer
        else:
            return RUDStudentSerializer


class ITManagerTermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
    permission_classes = [IsAuthenticated, IsItManager]

    http_method_names = ['get', 'post', 'put', 'patch', 'delete']


class ITManagerProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated, IsItManager]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProfessorFilter

    http_method_names = ['get', 'post', 'put', 'patch', 'delete']


class ITManagerFacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    http_method_names = ["get", "post", "put", "delete"]