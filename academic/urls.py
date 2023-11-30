from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (CourseViewSet, TermCourseViewSet, StudentListRetrieveSet, StudentAllowedCoursesView
, StudentRemainingTermsView, StudentCoursesReportView, ProfessorListRetrieveSet)

app_name = "academic"
router = DefaultRouter()
router.register('subjects', CourseViewSet, basename="subjects")
router.register('courses', TermCourseViewSet, basename="courses")
router.register('students', StudentListRetrieveSet, basename="students")
router.register('professors', ProfessorListRetrieveSet , basename="professors")

urlpatterns = [
    path('', include(router.urls)),
    path('student/<int:pk>/my-courses/', StudentAllowedCoursesView.as_view(), name="student-allowed-courses"),
    path('student/<int:pk>/remaining-terms/', StudentRemainingTermsView.as_view(), name="student-remaining-terms"),
    path('student/<int:pk>/pass-courses-report/', StudentCoursesReportView.as_view(), name="student-courses-report")
]