from django.http import HttpResponse
from .tasks import test_func
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsItManager
from .models import Student
from .serializers import CreatStudentSerializer
#
from rest_framework import viewsets
from rest_framework.response import Response
from .models import ITManager
from .serializers import ITmanagerSerializer


def test(request):
    test_func.delay()
    return HttpResponse('Done')

class CreatStudent(CreateAPIView):
    queryset = Student.objects.all()
    permission_classes = (IsAuthenticated, IsItManager)
    serializer_class = CreatStudentSerializer



#alikh
class FacultyViewSet(viewsets.ViewSet):
    def list(self, request):
        faculties = ITManager.objects.all()
        serializer = ITmanagerSerializer(faculties, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ITmanagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        faculty = self.get_object(pk)
        serializer = ITmanagerSerializer(faculty)
        return Response(serializer.data)

    def update(self, request, pk=None):
        faculty = self.get_object(pk)
        serializer = ITmanagerSerializer(faculty, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        faculty = self.get_object(pk)
        faculty.delete()
        return Response(status=204)

    def get_object(self, pk):
        try:
            return ITManager.objects.get(pk=pk)
        except ITManager.DoesNotExist:
            raise Http404