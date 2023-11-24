from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Count
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model
from .choices import *

User = get_user_model()


class Student(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True, related_name="student")
    supervisor = models.ForeignKey(to='Professor', on_delete=models.CASCADE, null=True, blank=True
                                   , related_name="student")
    major = models.ForeignKey(to='Major', on_delete=models.CASCADE, related_name="students")
    school = models.ForeignKey(to='School', on_delete=models.CASCADE, related_name="students")
    entrance_year = models.IntegerField()
    entrance_term = models.CharField(choices=ENTRANCE_TERM_CHOICES, max_length=6)
    military_status = models.CharField(choices=MILITARY_STATUS_CHOICES, max_length=20)
    courses = models.ManyToManyField(to='Course', through='Enrollment', blank=True)
    deleted_terms = models.ManyToManyField(to='Term', through='DeleteTerm', blank=True)

    @property
    def average_grade(self):
        enrollments = Enrollment.objects.get(student=self)
        average_grade = enrollments.aggregate(Avg("student_grade"))['student_grade__avg']
        return average_grade

    @property
    def sanavat(self):
        terms_count = Term.objects.filter(student=self).aggregate(term_count=Count('id'))['term_count']
        return terms_count


class Professor(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True)
    school = models.ForeignKey(to='School', on_delete=models.CASCADE, related_name="professors")
    past_courses = models.ManyToManyField(to='Course', blank=True)
    major = models.ForeignKey(to='Major', on_delete=models.CASCADE, related_name="professors")
    expertise = models.CharField(max_length=250, null=True, blank=True)
    rank = models.CharField(choices=PROFESSOR_RANK_CHOICES, max_length=20, null=True, blank=True)


class Course(models.Model):
    name = models.CharField(max_length=50)
    credits = models.FloatField(validators=(MinValueValidator(0),))
    type = models.CharField(choices=COURSE_TYPES, max_length=11)
    pre_requisites = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True
                                       , related_name="post_courses")
    co_requisites = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True
                                      , related_name="co_courses")
    schools = models.ManyToManyField(to='School', related_name="courses")


class Term(models.Model):
    students = models.ManyToManyField(to=Student, blank=True)
    professors = models.ManyToManyField(to='Professor', blank=True)
    courses = models.ManyToManyField(to='Course', through='TermCourse', blank=True)
    name = models.CharField(max_length=128)
    take_course_start_time = jmodels.jDateTimeField(blank=True, null=True)
    take_course_end_time = jmodels.jDateTimeField(blank=True, null=True)
    class_start_time = jmodels.jDateTimeField(blank=True, null=True)
    class_end_time = jmodels.jDateTimeField(blank=True, null=True)
    fix_course_start_time = jmodels.jDateTimeField(blank=True, null=True)
    fix_course_end_time = jmodels.jDateTimeField(blank=True, null=True)
    emergency_removal_end_time = jmodels.jDateTimeField(blank=True, null=True)
    exam_start_time = jmodels.jDateTimeField(blank=True, null=True)
    term_end_time = jmodels.jDateTimeField(blank=True, null=True)


class TermCourse(models.Model):
    class_date_time = jmodels.jDateTimeField()
    exam_date_time = jmodels.jDateTimeField()
    exam_site = models.CharField()
    capacity = models.PositiveIntegerField(validators=(MaxValueValidator(250),))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    professors = models.ManyToManyField(Professor)


class Major(models.Model):
    school = models.ForeignKey(to='School', on_delete=models.CASCADE, related_name="majors")
    name = models.CharField(max_length=128)
    units = models.IntegerField()
    stage = models.CharField(choices=STAGE_CHOICES, max_length=9)

    def __str__(self):
        return self.name


class Assistant(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True, related_name="assistant")
    school = models.OneToOneField(to='School', on_delete=models.CASCADE)
    major = models.OneToOneField(to='Major', on_delete=models.CASCADE)


class Enrollment(models.Model):
    student = models.ForeignKey(to='Student', on_delete=models.CASCADE, null=True, blank=True
                                , related_name="enrollments")
    course = models.ForeignKey(to='Course', on_delete=models.CASCADE, null=True, blank=True
                               , related_name="enrollments")
    taken_term = models.ForeignKey(to='Term', on_delete=models.CASCADE, null=True, blank=True
                                   , related_name="enrollments")
    course_condition = models.CharField(choices=COURSE_CONDITION_CHOICES, max_length=6)
    student_grade = models.IntegerField(null=True, blank=True)


class DeleteTerm(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="delete_terms")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="delete_terms")
    result = models.CharField(choices=REQUEST_RESULT_CHOICES, max_length=8, default="pending")
    student_comment = models.TextField()
    educational_deputy_comment = models.TextField()


class StudyEnrollmentRequest(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name="enrollment_requests")
    term = models.ForeignKey('Term', on_delete=models.CASCADE, related_name="enrollment_requests")
    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name="enrollment_requests")
    file = models.FileField(upload_to='study_enrollment_files/')


class ITManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id


class School(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class AddAndRemove(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="add_and_removes")
    added_term_course_id = models.ForeignKey('TermCourse', on_delete=models.CASCADE
                                             , related_name="added_courses")
    removed_term_course_id = models.ForeignKey('TermCourse', on_delete=models.CASCADE
                                               , related_name="removed_courses")
    status = models.CharField(choices=REQUEST_RESULT_CHOICES, max_length=8, default='pending')

    def __str__(self):
        return f"AddAndRemove #{self.id}"


class SelectUnit(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name="selected_units")
    term_course_id = models.ForeignKey('TermCourse', on_delete=models.CASCADE, related_name="selected_units")
    status = models.CharField(choices=REQUEST_RESULT_CHOICES, max_length=8, default='pending')

    def __str__(self):
        return f"SelectUnit #{self.id}"


class GradeRevisionRequest(models.Model):
    student = models.ForeignKey(to='Student', on_delete=models.CASCADE, related_name="grade_revision_requests")
    course = models.ForeignKey(to='Course', on_delete=models.CASCADE, related_name="grade_revision_requests")
    revision_message = models.TextField(null=True, blank=True)
    revision_answer = models.TextField(null=True, blank=True)


class EmergencyCourseDropRequest(models.Model):
    student = models.ForeignKey(to='Student', on_delete=models.CASCADE, related_name="emergency_course_drop_request")
    course = models.ForeignKey(to='Course', on_delete=models.CASCADE, related_name="emergency_course_drop_request")
    request_date = jmodels.jDateTimeField(auto_now_add=True)
    request_result = models.CharField(choices=REQUEST_RESULT_CHOICES, max_length=8, default='pending')
    student_explanation = models.TextField(null=True, blank=True)
    supervisor_explanation = models.TextField(null=True, blank=True)

