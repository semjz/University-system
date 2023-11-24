from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import ChangePasswordSerializer, LogoutSerializer
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.contrib.auth.tokens import PasswordResetTokenGenerator

User = get_user_model()
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request: Request):
        try:
            refresh_token = request.data["refresh"]
            refresh_token = RefreshToken(refresh_token)
            refresh_token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            error_message = {'error': str(e)}
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequest(APIView):
    permission_classes = (AllowAny,)

    def post(self, request: Request):
        reset_token = PasswordResetTokenGenerator().make_token(request.user)
        if not cache.get(request.user.user_id):
            cache.set(request.user.user_id, reset_token, CACHE_TTL)
            return Response(f"reset-token: {cache.get(request.user.user_id)}", status=status.HTTP_200_OK)
        else:
            return Response("A password reset request is already submitted", status=status.HTTP_400_BAD_REQUEST)


class PasswordResetAction(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ChangePasswordSerializer




