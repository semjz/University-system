from django.db import models

from academic.models import Course, TermCourse
from management.models import Term, Student, Professor
from utils.choices import REQUEST_RESULT_CHOICES, COURSE_CONDITION_CHOICES


class SelectUnit(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="selected_units")
    term_course_id = models.ForeignKey(TermCourse, on_delete=models.CASCADE, related_name="selected_units")
    status = models.CharField(choices=REQUEST_RESULT_CHOICES, max_length=8, default='pending')

    def __str__(self):
        return f"SelectUnit #{self.id}"


class AddAndRemove(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="add_and_removes")
    added_term_course_id = models.ForeignKey(TermCourse, on_delete=models.CASCADE
                                             , related_name="added_courses")
    removed_term_course_id = models.ForeignKey(TermCourse, on_delete=models.CASCADE
                                               , related_name="removed_courses")
    status = models.CharField(choices=REQUEST_RESULT_CHOICES, max_length=8, default='pending')

    def __str__(self):
        return f"AddAndRemove #{self.id}"


class EmergencyCourseDropRequest(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE, related_name="emergency_course_drop_request")
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, related_name="emergency_course_drop_request")
    request_date = models.DateTimeField(auto_now_add=True)
    request_result = models.CharField(choices=REQUEST_RESULT_CHOICES, max_length=8, default='pending')
    student_explanation = models.TextField(null=True, blank=True)
    supervisor_explanation = models.TextField(null=True, blank=True)


class StudyEnrollmentRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollment_requests")
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="enrollment_requests")
    school = models.ForeignKey("management.Faculty", on_delete=models.CASCADE, related_name="enrollment_requests")
    file = models.FileField(upload_to='study_enrollment_files/')


class Enrollment(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE, null=True, blank=True
                                , related_name="enrollments")
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, null=True, blank=True
                               , related_name="enrollments")
    taken_term = models.ForeignKey(to=Term, on_delete=models.CASCADE, null=True, blank=True
                                   , related_name="enrollments")
    course_condition = models.CharField(choices=COURSE_CONDITION_CHOICES, max_length=6)
    student_grade = models.IntegerField(null=True, blank=True)



