from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, StudentListRetrieveSet


app_name = "academic"
router = DefaultRouter()
router.register('subjects', CourseViewSet, basename="subjects")
router.register('students', StudentListRetrieveSet, basename="students")

urlpatterns = [
    path('', include(router.urls)),
]