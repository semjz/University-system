from django.db import models

from management.models import Professor, Student
from utils.choices import REQUEST_RESULT_CHOICES


class Term(models.Model):
    students = models.ManyToManyField(to=Student, blank=True, related_name="terms")
    professors = models.ManyToManyField(to=Professor, blank=True)
    courses = models.ManyToManyField(to="academic.Course", through='academic.TermCourse', blank=True)
    name = models.CharField(max_length=128)
    take_course_start_time = models.DateTimeField(blank=True, null=True)
    take_course_end_time = models.DateTimeField(blank=True, null=True)
    class_start_time = models.DateTimeField(blank=True, null=True)
    class_end_time = models.DateTimeField(blank=True, null=True)
    fix_course_start_time = models.DateTimeField(blank=True, null=True)
    fix_course_end_time = models.DateTimeField(blank=True, null=True)
    emergency_removal_end_time = models.DateTimeField(blank=True, null=True)
    exam_start_time = models.DateTimeField(blank=True, null=True)
    term_end_time = models.DateTimeField(blank=True, null=True)


class DeleteTerm(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="delete_terms")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="delete_terms")
    result = models.CharField(choices=REQUEST_RESULT_CHOICES, max_length=8, default="pending")
    student_comment = models.TextField()
    educational_deputy_comment = models.TextField()

