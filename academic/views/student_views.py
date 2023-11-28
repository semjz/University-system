from django.http import Http404
from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from academic.models import Course
from academic.permissions import IsAssistant, IsSameStudent
from academic.serializers.student import StudentAllowedCoursesSerializer
from management.models import Student
from management.filtersets import StudentFilterSet
from academic.serializers import StudentUpdateStudentSerializer, AssistantUpdateStudentSerializer
from management.serializers import RUDStudentSerializer

from rolepermissions.checkers import has_role
from authentication.roles import AssistantRole


class StudentListRetrieveSet(GenericViewSet
                             , mixins.ListModelMixin
                             , mixins.RetrieveModelMixin
                             , mixins.UpdateModelMixin):
    queryset = Student.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StudentFilterSet

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            if has_role(self.request.user, AssistantRole):
                return AssistantUpdateStudentSerializer

            else:
                return StudentUpdateStudentSerializer

        else:
            return RUDStudentSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "retrieve"]:
            return [IsAuthenticated(), (IsAssistant | IsSameStudent)()]

        if self.action in ["list"]:
            return [IsAuthenticated(), IsAssistant()]

    def perform_update(self, serializer):

        if self.request.data["user"].get("user_id"):
            if self.request.user.has_perm('authentication.can_modify_user_id'):
                serializer.save()
            else:
                raise PermissionDenied("You do not have permission to modify user_id.")
        else:
            serializer.save()

    class StudentAllowedCourses(APIView):
        permission_classes = (IsAuthenticated, IsSameStudent)

        def get_object(self, pk):
            try:
                return Student.objects.get(pk=pk)
            except Student.DoesNotExist:
                raise Http404

        def get(self, request, pk, format=None):
            student = self.get_object(pk)
            serializer = StudentAllowedCoursesSerializer(student.courses)
            return Response(serializer.data)



