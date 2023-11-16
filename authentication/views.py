from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, ChangePasswordSerializer
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import generics
from rest_framework.filters import SearchFilter
from .models import Assistant
from .serializers import AssistantSerializer


User = get_user_model()
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request:Request):
        try:
            refresh_token = request.data["refresh_token"]
            refresh_token = RefreshToken(refresh_token)
            refresh_token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class PasswordResetRequest(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request):
        reset_token = PasswordResetTokenGenerator().make_token(request.user)
        if not cache.get(request.user.user_id):
            cache.set(request.user.user_id, reset_token, CACHE_TTL)
            return Response(f"reset-token: {cache.get(request.user.user_id)}", status=status.HTTP_200_OK)
        else:
            return Response("A password reset request is already submitted", status=status.HTTP_400_BAD_REQUEST)


class PasswordResetAction(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class TestView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response("test", status=status.HTTP_200_OK)



class AssistantListCreateView(generics.ListCreateAPIView):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'employee_number', 'national_code', 'faculty', 'field']

class AssistantListView(generics.ListAPIView):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'employee_number', 'national_code', 'faculty', 'field']
