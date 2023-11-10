from django.db import models


MILITARY_STATUS_CHOICES = [
    ("permanent_exemption", 0),
    ("education_exemption", 1),
    ("end_of_service", 2),
    ("included", 3),
]
ENTRANCE_TERM_CHOICES = [
    ("Mehr", 1),
    ("Bahman", 2),
]
STAGE_CHOICES = [
    ("associate", 0),
    ("bachelor", 1),
    ("master", 2),
    ("phd", 3),
]


class Student(models.Model):
    # user = models.OneToOneField(to=User, on_delete=models.CASCADE, null=False, blank=False, primary_key=True)
    # supervisor = models.ForeignKey(to=Professor, on_delete=models.CASCADE, null=True, blank=True)
    # major = models.ForeignKey(to=Field, on_delete=models.CASCADE, null=False, blank=False)
    # school = models.ForeignKey(to=School, on_delete=models.CASCADE, null=False, blank=False)
    entrance_year = models.IntegerField(null=False, blank=False)
    entrance_term = models.CharField(choices=ENTRANCE_TERM_CHOICES, null=False, blank=False)
    military_status = models.CharField(choices=MILITARY_STATUS_CHOICES, null=False, blank=False)
    sanavat = models.IntegerField(null=False, blank=False)

    @property
    def average_grade(self):
        grades = Enrollment.objects.get(student_id=self.user.id).all()
        average_grade = sum(grades)/len(grades)
        return average_grade
        return True


class Field(models.Model):
    # school = models.ForeignKey(to=School, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=128, null=False, blank=False)
    units = models.IntegerField(null=False, blank=False)
    stage = models.CharField(choices=STAGE_CHOICES, null=False, blank=False)


class Term(models.Model):
    students = models.ManyToManyField(to=Student, null=True, blank=True)
    # professors = models.ManyToManyField(to=Professor, null=True, blank=True)  #Todo check for through_filed
    name = models.CharField(max_length=128, null=False, blank=False)
    take_course_start_time = models.DateTimeField(blank=True, null=True)
    take_course_end_time = models.DateTimeField(blank=True, null=True)
    class_start_time = models.DateTimeField(blank=True, null=True)
    class_end_time = models.DateTimeField(blank=True, null=True)
    fix_course_start_time = models.DateTimeField(blank=True, null=True)
    fix_course_end_time = models.DateTimeField(blank=True, null=True)
    emergency_removal_end_time = models.DateTimeField(blank=True, null=True)
    exam_start_time = models.DateTimeField(blank=True, null=True)
    term_end_time = models.DateTimeField(blank=True, null=True)


class EducationalDeputy(models.Model):
    # school = models.OneToOneField(to=School, on_delete=models.CASCADE, null=False, blank=False)
    # major = models.OneToOneField(to=Major, on_delete=models.CASCADE, null=False, blank=False)
    pass


class Enrollment(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE, null=True, blank=True)
    # course = models.ForeignKey(to=Course, on_delete=models.CASCADE, null=True, blank=True)
    taken_term = models.ForeignKey(to=Term, on_delete=models.CASCADE, null=True, blank=True)
    course_condition = models.CharField(max_length=128, null=False, blank=False)
    student_grade = models.IntegerField(null=True, blank=True)
