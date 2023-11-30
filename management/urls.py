from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ITManagerStudentViewSet, ITManagerTermViewSet, ITManagerProfessorViewSet, ITManagerFacultyViewSet

app_name = "management"
router = DefaultRouter()
router.register('student', ITManagerStudentViewSet, basename="admin-student")
router.register('term', ITManagerTermViewSet, basename="admin-term")
router.register('professor', ITManagerProfessorViewSet, basename="admin-professor")
router.register('faculty', ITManagerFacultyViewSet,  basename="admin-faculty")

urlpatterns = [
    path('', include(router.urls)),
]