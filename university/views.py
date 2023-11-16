from django.http import HttpResponse
from .tasks import test_func
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsItManager
from .models import Student
from .serializers import CreatStudentSerializer


def test(request):
    test_func.delay()
    return HttpResponse('Done')

class CreatStudent(CreateAPIView):
    queryset = Student.objects.all()
    permission_classes = (IsAuthenticated, IsItManager)
    serializer_class = CreatStudentSerializer
