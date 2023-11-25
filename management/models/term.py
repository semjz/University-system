from django.db import models

from management.models import Professor, Student
from utils.choices import REQUEST_RESULT_CHOICES


class Term(models.Model):
    name = models.CharField(max_length=128, unique=True)
    students = models.ManyToManyField(to=Student, blank=True, related_name='terms')
    professors = models.ManyToManyField(to='Professor', blank=True)
    courses = models.ManyToManyField(to='academic.Course', through='academic.TermCourse', blank=True, related_name='terms')
    take_course_start_time = models.DateTimeField()
    take_course_end_time = models.DateTimeField()
    class_start_time = models.DateField()
    class_end_time = models.DateField()
    fix_course_start_time = models.DateTimeField()
    fix_course_end_time = models.DateTimeField()
    emergency_removal_end_time = models.DateTimeField()
    exam_start_time = models.DateField()
    term_end_time = models.DateField()


class DeleteTerm(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="delete_terms")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="delete_terms")
    result = models.CharField(choices=REQUEST_RESULT_CHOICES, max_length=8, default="pending")
    student_comment = models.TextField()
    educational_deputy_comment = models.TextField()

