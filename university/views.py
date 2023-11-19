from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from .tasks import test_func
from .filters import ProfessorFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsItManager, IsAssistant
from .models import Student, Term, Course, Professor
from .serializers import CreateStudentSerializer, AdminTermSerializer, CourseSerializer, AdminProfessorSerializer


class CreateStudent(CreateAPIView):
    queryset = Student.objects.all()
    permission_classes = (IsAuthenticated, IsItManager)
    serializer_class = CreateStudentSerializer


class AdminTermViewSet(ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = AdminTermSerializer
    permission_classes = [IsAuthenticated, IsItManager]

    http_method_names = ['get', 'post', 'put', 'patch', 'delete']


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsItManager | IsAssistant]

    http_method_names = ['get', 'post', 'put', 'patch', 'delete']


class AdminProfessorViewSet(ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = AdminProfessorSerializer
    permission_classes = [IsAuthenticated, IsItManager]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProfessorFilter

    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
