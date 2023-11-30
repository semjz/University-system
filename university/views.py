from django.http import HttpResponse
from .tasks import test_func
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsItManager
from .serializers import CreatStudentSerializer
##
from rest_framework import viewsets
from .serializers import SchoolSerializer
from .models import School

from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from .models import Student, Professor
from .serializers import StudentSerializer, ProfessorSerializer

def test(request):
    test_func.delay()
    return HttpResponse('Done')

class CreatStudent(CreateAPIView):
    queryset = Student.objects.all()
    permission_classes = (IsAuthenticated, IsItManager)
    serializer_class = CreatStudentSerializer



#alikh
class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    http_method_names = ["get", "post", "put", "delete"]


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        # اعمال فیلترها اگر معاون آموزشی نیست
        if not self.request.user.is_staff:
            self.queryset = self.queryset.filter(id=self.request.user.id)
        return super().get_queryset()


class ProfessorViewSet(ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        # اعمال فیلترها اگر معاون آموزشی نیست
        if not self.request.user.is_staff:
            self.queryset = self.queryset.filter(id=self.request.user.id)
        return super().get_queryset()