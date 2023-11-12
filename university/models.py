from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Count
from django_jalali.db import models as jmodels


COURSE_TYPES = [
    ("general", "General"),
    ("specialized", "Specialized"),
    ("core", "Core"),
    ("optional", "Optional")
]

MILITARY_STATUS_CHOICES = [
    ("permanent_exemption", "Permanent Exemption"),
    ("education_exemption", "Education Exemption"),
    ("end_of_service", "End of Service"),
    ("included", "Included"),
]
ENTRANCE_TERM_CHOICES = [
    ("Mehr", "Mehr"),
    ("Bahman", "Bahman"),
]
STAGE_CHOICES = [
    ("associate", "Associate"),
    ("bachelor", "Bachelor"),
    ("master", "Master"),
    ("phd", "PHD"),
]
COURSE_CONDITION_CHOICES = [
    ("failed", "Failed"),
    ("passed", "Passed"),
]

PROFESSOR_RANK_CHOICES = [
    ('instructor', 'Instructor'),  # morabi
    ('assistant_professor', 'Assistant Professor'),  # ostadyar
    ('associate_professor', 'Associate Professor'),  # daneshyar
    ('full_professor', 'Full Professor'),  # ostad tamam
]

REQUEST_RESULT_CHOICES = [
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('pending', 'Pending'),
]


class Student(models.Model):
    user = models.OneToOneField(to='User', on_delete=models.CASCADE, primary_key=True)
    supervisor = models.ForeignKey(to='Professor', on_delete=models.CASCADE, null=True, blank=True)
    major = models.ForeignKey(to='Major', on_delete=models.CASCADE)
    school = models.ForeignKey(to='School', on_delete=models.CASCADE)
    entrance_year = models.IntegerField()
    entrance_term = models.CharField(choices=ENTRANCE_TERM_CHOICES)
    military_status = models.CharField(choices=MILITARY_STATUS_CHOICES)
    courses = models.ManyToManyField(to='Course', through='Enrollment', null=True, blank=True)
    deleted_terms = models.ManyToManyField(to='Term', through='DeleteTerm', null=True, blank=True)

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
    user = models.OneToOneField(to='User', on_delete=models.CASCADE, primary_key=True)
    school = models.ForeignKey(to='School', on_delete=models.CASCADE)
    past_courses = models.ManyToManyField(to='Course', null=True, blank=True)
    major = models.ForeignKey(to='Major', on_delete=models.CASCADE)
    expertise = models.CharField(max_length=250, null=True, blank=True)
    rank = models.CharField(choices=PROFESSOR_RANK_CHOICES, null=True, blank=True)


class Course(models.Model):
    name = models.CharField(max_length=50)
    credits = models.FloatField(validators=(MinValueValidator(0),))
    type = models.CharField(choices=COURSE_TYPES)
    pre_requisites = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True
                                       , related_name="post_courses")
    co_requisites = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True
                                      , related_name="co_courses")
    schools = models.ManyToManyField(to='School')


class Term(models.Model):
    students = models.ManyToManyField(to=Student, null=True, blank=True)
    professors = models.ManyToManyField(to='Professor', null=True, blank=True)
    courses = models.ManyToManyField(to='Course', through='TermCourse', null=True, blank=True)
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
    class_date_time = models.DateTimeField()
    exam_date_time = models.DateTimeField()
    exam_site = models.CharField()
    capacity = models.PositiveIntegerField(validators=(MaxValueValidator(250),))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    professors = models.ManyToManyField(Professor)


class Major(models.Model):
    school = models.ForeignKey(to='School', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    units = models.IntegerField()
    stage = models.CharField(choices=STAGE_CHOICES)


class Assistant(models.Model):
    user = models.OneToOneField(to='User', on_delete=models.CASCADE, primary_key=True)
    school = models.OneToOneField(to='School', on_delete=models.CASCADE)
    major = models.OneToOneField(to='Major', on_delete=models.CASCADE)


class Enrollment(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(to='Course', on_delete=models.CASCADE, null=True, blank=True)
    taken_term = models.ForeignKey(to=Term, on_delete=models.CASCADE, null=True, blank=True)
    course_condition = models.CharField(choices=COURSE_CONDITION_CHOICES)
    student_grade = models.IntegerField(null=True, blank=True)


class DeleteTerm(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    result = models.CharField(choices=REQUEST_RESULT_CHOICES)
    student_comment = models.TextField()
    educational_deputy_comment = models.TextField()


class StudyEnrollmentRequest(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    term = models.ForeignKey('Term', on_delete=models.CASCADE)
    school = models.ForeignKey('School', on_delete=models.CASCADE)
    file = models.FileField(upload_to='study_enrollment_files/')


class GradeRevisionRequest(models.Model):
    student = models.ForeignKey(to='Student', on_delete=models.CASCADE)
    course = models.ForeignKey(to='Course', on_delete=models.CASCADE)
    revision_message = models.TextField(null=True, blank=True)
    revision_answer = models.TextField(null=True, blank=True)


class EmergencyCourseDropRequest(models.Model):
    student = models.ForeignKey(to='Student', on_delete=models.CASCADE)
    course = models.ForeignKey(to='Course', on_delete=models.CASCADE)
    request_date = jmodels.jDateTimeField(auto_now_add=True)
    request_result = models.CharField(choices=REQUEST_RESULT_CHOICES, default='pending')
    student_explanation = models.TextField(null=True, blank=True)
    supervisor_explanation = models.TextField(null=True, blank=True)

