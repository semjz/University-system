from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, TermCourseViewSet, StudentListRetrieveSet

app_name = "academic"
router = DefaultRouter()
router.register('subjects', CourseViewSet, basename="subjects")
router.register('courses', TermCourseViewSet, basename="courses")
router.register('students', StudentListRetrieveSet, basename="students")

urlpatterns = [
    path('', include(router.urls)),
]