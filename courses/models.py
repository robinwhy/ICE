from django.db import models
from django.contrib.auth.models import User
from instructors.models import Instructor
from learners.models import Learner
import datetime


# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=200)
    def __str__(self):
        return self.category


class Course(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    open_status = models.BooleanField(default=True)
    thumb = models.ImageField(default='default.png', blank=True)
    CECU = models.IntegerField(default=1)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE,null=True, blank=True)

    # progress = models.ManyToManyField(Learner, through='Progress')

    # one-to-many
    instructor_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.description


class Module(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    Course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    order = models.PositiveIntegerField(null=True, blank= True)
    question_number = models.IntegerField(default = 0)
    pass_score = models.IntegerField(default=0, null=True, blank= True)
    def __str__(self):
        return self.title


class Component(models.Model):
    title = models.CharField(max_length=100)
    text_content = models.TextField(blank=True, null=True)
    image_content = models.ImageField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    order = models.PositiveIntegerField(null=True, blank= True)
    Course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    Module = models.ForeignKey(Module, null=True, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.title


class Progress(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    latest_progress = models.IntegerField(default=1)

    def __str__(self):
        return self.learner.username + " at " + self.course.title


class QuizQuestion(models.Model):
    question_text = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=0)
    selected = models.BooleanField(default=False)
    module= models.ForeignKey(Module, on_delete=models.CASCADE, blank= True, null= True)

    def __str__(self):
        return self.question_text


class QuizChoice(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class QuizResult(models.Model):
    total_score = models.IntegerField(default=0)
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.learner.username + " scored " + str(self.total_score) + " in the latest quiz of "+self.course.title


class EnrollmentHistory(models.Model):
    completed = models.BooleanField(default=False)
    date_completed = models.DateField("Date", default=datetime.date.today)
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        if self.completed:
            return self.learner.username + " completed " + self.course.title + " on " + str(self.date_completed)
        else:
            return self.learner.username + " is currently studying " + self.course.title
