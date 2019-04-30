from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from courses.models import Course, Module, Component, QuizQuestion, QuizChoice
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from .forms import *
from instructors.models import *
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User, Group
import urllib.request

instructor_email = 'loganwanghk@gmail.com'


def is_member(user):
    return user.groups.filter(name='instructor').exists()


def send_email(request):
    if request.method == 'POST':
        form = SendEmailForm(request.POST)
        if form.is_valid():
            global instructor_email
            instructor_email = form.cleaned_data.get('instructor_email')
            message = render_to_string('instructor_account_activation_email.html', {
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(instructor_email)),
                'token': account_activation_token.make_token(instructor_email),
            })
            send_mail(
                'Activate your account',
                message,
                settings.EMAIL_HOST_USER,
                [instructor_email],
            )
            return redirect('instructors:waitforactivation')
    else:
        form = SendEmailForm()
    return render(request, 'instructor_signup.html', {'form': form})


def waitforactivation(request):
    return render(request, 'waitforactivation.html')


def activate(request, uidb64, token):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            autobiography = form.cleaned_data.get('autobiography')
            user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                            last_name=last_name,
                                            email=instructor_email)
            instructor = Instructor.objects.create(username=username)
            my_group = Group.objects.get(name='instructor')
            my_group.user_set.add(user)
            return redirect('instructors:activate_complete')
    else:
        form = SignupForm()
    return render(request, 'instructor_activate.html', {'form': form})


def activate_complete(request):
    return render(request, 'instructor_activate_complete.html')


@login_required
@user_passes_test(is_member)
def instructor_course_list(request):
    current_user = request.user
    courses = Course.objects.filter(instructor_user_id=current_user.id).order_by('date');
    # courses = Course.objects.filter(instructor_id=1).order_by('date');
    return render(request, 'instructor_course_list.html', {'courses': courses})


@login_required
@user_passes_test(is_member)
def instructor_modules(request, course_id):
    course = Course.objects.get(id=course_id)
    modules = Module.objects.filter(Course_id=course.id).order_by('order')
    return render(request, 'instructor_module_list.html', {'course': course, 'modules': modules})


@login_required
@user_passes_test(is_member)
def instructor_components(request, moduleid):
    module = Module.objects.get(id=moduleid)
    components = Component.objects.filter(Module_id=module.id).order_by('order')
    return render(request, 'instructor_module_detail.html', {'components': components, 'module': module})


@login_required
@user_passes_test(is_member)
def add_course(request):
    if request.method == 'POST':
        form = createCourse(request.POST, request.FILES)
        if form.is_valid():
            # save course to DB
            instance = form.save(commit=False)
            instance.instructor_user_id = request.user.id
            # instance.instructor_id = request.user.id
            instance.save()
            return redirect('instructors:list')
    else:
        form = createCourse()
        return render(request, 'add_course.html', {'form': form})


@login_required
@user_passes_test(is_member)
def add_module(request, courseid):
    if request.method == 'POST':
        form = createModule(request.POST, request.FILES)
        if form.is_valid():
            # save module to DB
            instance = form.save(commit=False)
            course = Course.objects.get(id=courseid)
            instance.Course = course
            if (instance.order is None):
                order = Module.objects.filter(Course=course).count() + 1
                instance.order = order
            if (Module.objects.filter(order=instance.order, Course_id=courseid).exists()):
                collision_module = Module.objects.get(Course=course, order=instance.order)
                collision_module.order = Module.objects.filter(Course=course).count() + 1
                collision_module.save()
            instance.save()
            return redirect('instructors:instructor-modules', course_id=course.id)
    else:
        form = createModule()
        return render(request, 'add_module.html', {'form': form, 'courseid': courseid})

@login_required
@user_passes_test(is_member)
def reorder_module(request, courseid):
    if request.method == 'POST':
        form = reorderModule(request.POST, request.FILES, courseid=courseid)
        if form.is_valid():
            # save component to DB
            moduleid = form.cleaned_data.get('module')
            order = form.cleaned_data.get('order')
            module = Module.objects.get(id=moduleid)
            if (order is not None):
                if (Module.objects.filter(Course_id=courseid, order=order).exists()):
                    collision_module = Module.objects.get(Course_id=courseid, order=order)
                    collision_module.order = module.order
                    collision_module.save()
                module.order = order
            module.save()
            return redirect('instructors:instructor-modules', course_id=courseid)
    else:
        form = reorderModule(courseid=courseid)
        return render(request, 'reorder_module.html', {'form': form, 'courseid': courseid})

@login_required
@user_passes_test(is_member)
def add_component(request, moduleid):
    module = Module.objects.get(id=moduleid)
    course_id = module.Course_id
    if request.method == 'POST':
        form = addComponent(request.POST, request.FILES, courseid=course_id)
        if form.is_valid():
            # save component to DB
            componentids = form.cleaned_data.get('components')
            order = form.cleaned_data.get('order')
            for id in componentids:
                component = Component.objects.get(id=id)
                component.Module_id = moduleid
                if (order is None):
                    order = Component.objects.filter(Course_id=course_id, Module_id=moduleid).count() + 1
                    component.order = order
                else:
                    if (Component.objects.filter(Course_id=course_id, Module_id=moduleid, order=order).exists()):
                        collision_component = Component.objects.get(Course_id=course_id, Module_id=moduleid, order=order)
                        collision_component.order = Component.objects.filter(Course_id=course_id,
                                                                          Module_id=moduleid).count() + 1
                        collision_component.save()
                    component.order = order
                component.save()
            return redirect('instructors:instructor-module-detail', moduleid=module.id)
    else:
        form = addComponent(courseid=course_id)
        return render(request, 'add_component.html', {'form': form, 'moduleid': moduleid})


@login_required
@user_passes_test(is_member)
def reorder_component(request, moduleid):
    module = Module.objects.get(id=moduleid)
    course_id = module.Course_id
    if request.method == 'POST':
        form = reorderComponent(request.POST, request.FILES, courseid=course_id, moduleid=moduleid)
        if form.is_valid():
            # save component to DB
            componentid = form.cleaned_data.get('components')
            order = form.cleaned_data.get('order')
            component = Component.objects.get(id=componentid)
            if (order is not None):
                if (Component.objects.filter(Course_id=course_id, Module_id=moduleid, order=order).exists()):
                    collision_component = Component.objects.get(Course_id=course_id, Module_id=moduleid, order=order)
                    collision_component.order = component.order
                    collision_component.save()
                component.order = order
            component.save()
            return redirect('instructors:instructor-module-detail', moduleid=module.id)
    else:
        form = reorderComponent(courseid=course_id, moduleid=moduleid)
        return render(request, 'reorder_component.html', {'form': form, 'moduleid': moduleid})


@login_required
@user_passes_test(is_member)
def add_quiz(request, moduleid):
    module = Module.objects.get(id = moduleid)
    course_id = module.Course_id
    if request.method == 'POST':
        form = createQuiz(request.POST, courseid=course_id)
        if form.is_valid():
            # switch selected to True
            questionids = form.cleaned_data.get('questions')
            pass_score = form.cleaned_data.get('pass_score')
            question_number = form.cleaned_data.get('question_number')
            for id in questionids:
                question = QuizQuestion.objects.get(id=id)
                question.selected = True
                question.module_id = moduleid
                question.save()
            module = Module.objects.get(id=moduleid)
            module.pass_score = pass_score
            module.question_number = question_number
            module.save()
            return redirect('instructors:instructor-module-detail', moduleid=module.id)
    else:
        form = createQuiz(courseid=course_id)
        return render(request, 'add_quiz.html', {'form': form, 'moduleid': moduleid})


@login_required
@user_passes_test(is_member)
def instructor_view_quiz(request, moduleid):
    module = Module.objects.get(id=moduleid)
    questions = QuizQuestion.objects.filter(course_id=module.Course_id);
    # choices = QuizChoice.objects.filter(moduleid_id=moduleid);
    choices = {}
    for question in questions:
        if question.selected == True:
            answers = QuizChoice.objects.filter(question_id=question.id)
            choices[question] = answers

    return render(request, 'instructor_view_quiz.html',
                  {'questions': questions, 'choices': choices, 'module_title': module.title})
