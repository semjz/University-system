from django.urls import path
from .views import LogoutView, PasswordResetRequest, PasswordResetAction
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

app_name = "authentication"
urlpatterns = [
    path("change-password-request/", PasswordResetRequest.as_view(), name="reset-password-request"),
    path("change-password-action/", PasswordResetAction.as_view(), name="reset-password-action"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
]