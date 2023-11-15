from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsItManager
from .models import Student
from .serializers import CreatStudentSerializer


class CreatStudent(CreateAPIView):
    queryset = Student.objects.all()
    permission_classes = (IsAuthenticated, IsItManager)
    serializer_class = CreatStudentSerializer
