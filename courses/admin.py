from django.contrib import admin
from .models import Course, Module, Component, QuizChoice, QuizQuestion,Progress, QuizResult, EnrollmentHistory, Category

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Component)
admin.site.register(QuizChoice)
admin.site.register(QuizQuestion)
admin.site.register(Progress)
admin.site.register(QuizResult)
admin.site.register(EnrollmentHistory)
admin.site.register(Category)