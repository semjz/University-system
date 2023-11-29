from django.http import HttpResponse
from .tasks import test_func
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsItManager
from .models import Student
from .serializers import CreatStudentSerializer
##
from rest_framework import viewsets
from .serializers import SchoolSerializer


def test(request):
    test_func.delay()
    return HttpResponse('Done')

class CreatStudent(CreateAPIView):
    queryset = Student.objects.all()
    permission_classes = (IsAuthenticated, IsItManager)
    serializer_class = CreatStudentSerializer



#alikh
class SchoolViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = SchoolSerializer
    http_method_names = ["get", "post", "put", "delete"]


