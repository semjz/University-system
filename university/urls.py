from django.urls import path
from .views import CreatStudent

app_name = "university"
urlpatterns = [
    path("admin/students/", CreatStudent.as_view(), name="create-student")
]
