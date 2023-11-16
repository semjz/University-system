from django.urls import path
from .views import (RegisterView, LogoutView, PasswordResetRequest, PasswordResetAction, TestView,AssistantListCreateView,
                    AssistantListView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


app_name = "authentication"
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("change-password-request/", PasswordResetRequest.as_view(), name="reset-password-request"),
    path("change-password-action/<int:pk>/", PasswordResetAction.as_view(), name="reset-password-action"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("test/", TestView.as_view(), name="test"),
    path('api/v1/admin/assistants/', AssistantListCreateView.as_view(), name='assistant-list-create'),
    path('api/v1/admin/assistants/list/', AssistantListView.as_view(), name='assistant-list'),
]



