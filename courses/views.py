from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Course, Module, Component
from django.contrib.auth.decorators import login_required

def instructor_course_list(request):
    courses = Course.objects.all().order_by('date');
    return render(request, 'courses/../templates/instructor_course_list.html', {'courses': courses})

