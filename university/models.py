from django.db import models
from django.db.models import Avg, Count
from django_jalali.db import models as jmodels

MILITARY_STATUS_CHOICES = [
    ("permanent_exemption", "permanent_exemption"),
    ("education_exemption", "education_exemption"),
    ("end_of_service", "end_of_service"),
    ("included", "included"),
]
ENTRANCE_TERM_CHOICES = [
    ("Mehr", "Mehr"),
    ("Bahman", "Bahman"),
]
STAGE_CHOICES = [
    ("associate", "associate"),
    ("bachelor", "bachelor"),
    ("master", "master"),
    ("phd", "phd"),
]
COURSE_CONDITION_CHOICES = [
    ("failed", "failed"),
    ("passed", "passed"),
]

DELETE_TERM_STATUS = [
    ("deleted", "deleted"),
    ("not_deleted", "not_deleted"),
]


class Student(models.Model):
    user = models.OneToOneField(to='User', on_delete=models.CASCADE, null=False, blank=False, primary_key=True)
    supervisor = models.ForeignKey(to='Professor', on_delete=models.CASCADE, null=True, blank=True)
    major = models.ForeignKey(to='Field', on_delete=models.CASCADE, null=False, blank=False)
    school = models.ForeignKey(to='School', on_delete=models.CASCADE, null=False, blank=False)
    entrance_year = models.IntegerField(null=False, blank=False)
    entrance_term = models.CharField(choices=ENTRANCE_TERM_CHOICES, null=False, blank=False)
    military_status = models.CharField(choices=MILITARY_STATUS_CHOICES, null=False, blank=False)
    courses = models.ManyToManyField(to='Course', through='Enrollment', null=True, blank=True)

    @property
    def average_grade(self):
        enrollments = Enrollment.objects.get(student=self)
        average_grade = enrollments.aggregate(Avg("student_grade"))['student_grade__avg']
        return average_grade

    @property
    def sanavat(self):
        terms_count = Term.objects.filter(student=self).aggregate(term_count=Count('id'))['term_count']
        return terms_count


class Field(models.Model):
    school = models.ForeignKey(to='School', on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=128, null=False, blank=False)
    units = models.IntegerField(null=False, blank=False)
    stage = models.CharField(choices=STAGE_CHOICES, null=False, blank=False)


class Term(models.Model):
    students = models.ManyToManyField(to=Student, null=True, blank=True)
    professors = models.ManyToManyField(to='Professor', null=True, blank=True)
    courses = models.ManyToManyField(to='Course', through='TermicCourse', null=True, blank=True)
    name = models.CharField(max_length=128, null=False, blank=False)
    take_course_start_time = jmodels.jDateTimeField(blank=True, null=True)
    take_course_end_time = jmodels.jDateTimeField(blank=True, null=True)
    class_start_time = jmodels.jDateTimeField(blank=True, null=True)
    class_end_time = jmodels.jDateTimeField(blank=True, null=True)
    fix_course_start_time = jmodels.jDateTimeField(blank=True, null=True)
    fix_course_end_time = jmodels.jDateTimeField(blank=True, null=True)
    emergency_removal_end_time = jmodels.jDateTimeField(blank=True, null=True)
    exam_start_time = jmodels.jDateTimeField(blank=True, null=True)
    term_end_time = jmodels.jDateTimeField(blank=True, null=True)


class EducationalDeputy(models.Model):
    school = models.OneToOneField(to='School', on_delete=models.CASCADE, null=False, blank=False)
    major = models.OneToOneField(to='Major', on_delete=models.CASCADE, null=False, blank=False)


class Enrollment(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(to='Course', on_delete=models.CASCADE, null=True, blank=True)
    taken_term = models.ForeignKey(to=Term, on_delete=models.CASCADE, null=True, blank=True)
    course_condition = models.CharField(choices=COURSE_CONDITION_CHOICES, null=False, blank=False)
    student_grade = models.IntegerField(null=True, blank=True)





class DeleteTerm(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    result = models.CharField(choices=DELETE_TERM_STATUS, null=False, blank=False)
    student_comment = models.TextField()
    educational_deputy_comment = models.TextField()

class StudyEnrollmentRequest(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    term = models.ForeignKey('Term', on_delete=models.CASCADE)
    school = models.ForeignKey('school', on_delete=models.CASCADE)
    file = models.FileField(upload_to='study_enrollment_files/')



