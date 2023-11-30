from django.contrib.auth import get_user_model
from authentication.serializers import FullUpdateUserSerializer, RestrictUpdateUserSerializer
from management.serializers import CreateProfessorSerializer


User = get_user_model()


class AssistantUpdateProfessorSerializer(CreateProfessorSerializer):
    user = FullUpdateUserSerializer()


class ProfessorUpdateProfessorSerializer(CreateProfessorSerializer):
    user = RestrictUpdateUserSerializer()

