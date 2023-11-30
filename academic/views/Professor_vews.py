from rest_framework import mixins, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rolepermissions.checkers import has_role

from academic.permissions import IsAssistant,IsSameProfessor
from academic.serializers import AssistantUpdateProfessorSerializer,ProfessorUpdateProfessorSerializer
from authentication.roles import AssistantRole
from management.filtersets import ProfessorFilter
from management.models import Professor
from management.serializers import ProfessorSerializer


class ProfessorListRetrieveSet(GenericViewSet
                             , mixins.ListModelMixin
                             , mixins.RetrieveModelMixin
                             , mixins.UpdateModelMixin):
    queryset = Professor.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProfessorFilter

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            if has_role(self.request.user, AssistantRole):
                return AssistantUpdateProfessorSerializer

            else:
                return ProfessorUpdateProfessorSerializer

        else:
            return ProfessorSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "retrieve"]:
            return [IsAuthenticated(), (IsAssistant | IsSameProfessor)()]

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
