from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from .tasks import test_func
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsItManager, IsAssistant
from .models import Student, Term, Course
from .serializers import CreateStudentSerializer, TermSerializer, CourseSerializer


class CreateStudent(CreateAPIView):
    queryset = Student.objects.all()
    permission_classes = (IsAuthenticated, IsItManager)
    serializer_class = CreateStudentSerializer


class TermViewSet(ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
    permission_classes = [IsAuthenticated, IsItManager]

    http_method_names = ['get', 'post', 'put', 'patch', 'delete']


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsItManager | IsAssistant]

    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
