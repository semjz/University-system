from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Pyvengers University project",
        default_version='v1',
        description="Pyvengers University project's APIs",
    ),
    public=True,
    permission_classes=[permissions.AllowAny]  # This should be changed to permitted users
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Here you should implement your app's urls
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('users/', include('authentication.urls'))
]
