from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ITManagerStudentViewSet

app_name = "university"
router = DefaultRouter()
router.register('admin/student', ITManagerStudentViewSet, basename="admin-student")

urlpatterns = [
    path('', include(router.urls)),
]