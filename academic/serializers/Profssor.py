from django.contrib.auth import get_user_model
from authentication.serializers import FullUpdateUserSerializer, StudentUpdateUserSerializer
from management.serializers import ProfessorSerializer


User = get_user_model()


class AssistantUpdateProfessorSerializer(ProfessorSerializer):
    user = FullUpdateUserSerializer()


class ProfessorUpdateProfessorSerializer(AssistantUpdateProfessorSerializer):
    user = StudentUpdateUserSerializer()

