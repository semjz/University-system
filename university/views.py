from django.http import HttpResponse
from .tasks import test_func
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsItManager
from .models import Student
from .serializers import CreatStudentSerializer


def test(request):
    test_func.delay()
    return HttpResponse('Done')


class ITManagerStudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    permission_classes = (IsAuthenticated, IsItManager)
    serializer_class = CreatStudentSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def perform_destroy(self, instance):
        instance.user.delete()

