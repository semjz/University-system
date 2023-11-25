from django.db import models
from management.models import Student
from academic.models import Course


class GradeRevisionRequest(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE, related_name="grade_revision_requests")
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, related_name="grade_revision_requests")
    revision_message = models.TextField(null=True, blank=True)
    revision_answer = models.TextField(null=True, blank=True)



