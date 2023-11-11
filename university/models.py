from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.


COURSE_TYPES = [("general", "General"), ("specialized", "Specialized")
    , ("core", "Core"), ("optional", "Optional")]


class Course(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    credits = models.FloatField(blank=False, null=False, validators=(MinValueValidator(0),))
    type = models.CharField(choices=COURSE_TYPES, blank=False, null=False)
    pre_requisites = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True)
    co_requisites = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True)
    # school = models.ManyToManyField(School)
