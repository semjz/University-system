from django.http import HttpResponse
from .tasks import test_func
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsItManager
from .models import Student
from .serializers import StudentSerializer
from django_filters import rest_framework as filters
import university.filtersets as filtersets


def test(request):
    test_func.delay()
    return HttpResponse('Done')


class ITManagerStudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    permission_classes = (IsAuthenticated, IsItManager)
    serializer_class = StudentSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = filtersets.StudentFilterSet

    def perform_destroy(self, instance):
        instance.user.delete()






