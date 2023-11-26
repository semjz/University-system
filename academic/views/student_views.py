from django_filters import rest_framework as filters
from rest_framework import mixins, status
from rest_framework.exceptions import PermissionDenied

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from academic.permissions import IsAssistant, IsSameStudent
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
    permission_classes = (IsAuthenticated, IsAssistant | IsSameStudent)

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

        if self.request.data["user"]["user_id"]:
            if self.request.user.has_perm('management.can_modify_user_id'):
                serializer.save()
            else:
                raise PermissionDenied("You do not have permission to modify user_id.")
        else:
            serializer.save()

