from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from management.models import Term

from utils.choices import COURSE_TYPES


class Course(models.Model):

    name = models.CharField(max_length=50, unique=True)
    credits = models.FloatField(validators=(MinValueValidator(0),))
    type = models.CharField(choices=COURSE_TYPES, max_length=11)
    pre_requisites = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="post_courses")
    co_requisites = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="co_courses")
    schools = models.ManyToManyField(to="management.Faculty", related_name="courses")

    def __str__(self):
        return f"{self.name}"


class TermCourse(models.Model):

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'term', 'class_date_time']
                                    , name='unique termcourse')
        ]

    class_date_time = models.DateTimeField()
    exam_date_time = models.DateTimeField(blank=True, null=True)
    exam_site = models.CharField()
    capacity = models.PositiveIntegerField(validators=(MaxValueValidator(250),))
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    professor = models.ForeignKey("management.Professor", on_delete=models.CASCADE)
