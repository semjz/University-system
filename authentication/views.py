from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from .serializers import ChangePasswordActionSerializer, ChangePasswordRequestSerializer, LogoutSerializer
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404


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


class PasswordResetRequest(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ChangePasswordRequestSerializer

    def post(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=serializer.validated_data["email"])
        reset_token = PasswordResetTokenGenerator().make_token(user)
        try:
            cache.set(reset_token, user.user_id, CACHE_TTL)
            send_mail(
                "Password Reset Code",
                f"Your reset password code: {reset_token}",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return Response("reset token was emailed successfully!", status.HTTP_200_OK)
        except Exception as e:
            error_message = {'error': str(e)}
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetAction(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ChangePasswordActionSerializer

    def put(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_token = serializer.validated_data["reset_token"]
        if not cache.get(reset_token):
            return Response("reset token is wrong or expired!", status=status.HTTP_400_BAD_REQUEST)
        else:
            user_id = cache.get(reset_token)
            user = get_object_or_404(User, user_id=user_id)
            user.set_password(serializer.validated_data["new_pass"])
            user.save()
            return Response("password was changed successfully", status.HTTP_200_OK)




