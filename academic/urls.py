from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, TermCourseViewSet

app_name = "academic"
router = DefaultRouter()
router.register('subjects', CourseViewSet, basename="subjects")
router.register('courses', TermCourseViewSet, basename="courses")

urlpatterns = [
    path('', include(router.urls)),
]