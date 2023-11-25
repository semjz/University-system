from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet

app_name = "academic"
router = DefaultRouter()
router.register('subjects', CourseViewSet, basename="subjects")

urlpatterns = [
    path('', include(router.urls)),
]