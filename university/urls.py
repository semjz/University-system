from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateStudent, AdminTermViewSet, CourseViewSet, AdminProfessorViewSet

router = DefaultRouter()
router.register('admin/term', AdminTermViewSet)
router.register('admin/professor', AdminProfessorViewSet)
router.register('courses', CourseViewSet, basename='course')

app_name = "university"
urlpatterns = [
    path("admin/students/", CreateStudent.as_view(), name="create-student"),
    path('', include(router.urls)),
]
