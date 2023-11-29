from django.urls import path
from .views import CreatStudent
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SchoolViewSet
app_name = "university"
urlpatterns = [
    path("admin/students/", CreatStudent.as_view(), name="create-student")

]
router = DefaultRouter()
router.register(r'admin/Schools', SchoolViewSet, basename='school')

urlpatterns = [
    path('', include(router.urls)),
]

