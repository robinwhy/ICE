from django.db import models
from learners.models import Learner
from courses.models import Course
# Create your models here.
class Progress(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="course")
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, verbose_name="learner")
    progress=models.IntegerField(default=1)