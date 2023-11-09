from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
import uuid

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
        reset_token = uuid.uuid4()
        if not cache.get(request.user.user_id):
            cache.set(request.user.user_id, reset_token, CACHE_TTL)
            return Response(f"reset-token: {cache.get(request.user.user_id)}", status=status.HTTP_200_OK)
        else:
            return Response("A password reset request is already submitted", status=status.HTTP_400_BAD_REQUEST)


class PasswordResetAction(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request:Request):
        if cache.get(request.user.user_id):
            if request.data["reset_token"] == cache.get(request.user.user_id):
                new_password = request.data["new_password"]
                request.user.set_password(new_password)
                return Response("Password successfully changed!", status=status.HTTP_200_OK)
            else:
                return Response("Reset token is wrong!", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("No password reset request for this user!", status=status.HTTP_400_BAD_REQUEST)


class TestView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response("test", status=status.HTTP_200_OK)


