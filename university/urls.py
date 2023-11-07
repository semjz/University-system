from django.urls import path
from university.views import TestView

urlpatterns = [
    path('books/', TestView.as_view()),
]
