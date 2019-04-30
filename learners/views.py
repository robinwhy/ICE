from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required, user_passes_test
from itertools import chain
from django.template.loader import render_to_string
from .forms import *
from .models import *
from courses.models import *
from courses.forms import *
from learners.models import *
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_text,force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User,Group
import urllib.request
import json,random

def is_member(user):
    return user.groups.filter(name='learner').exists()
staff_id= "00003297"
first_name= "Sid"
last_name= "Miglani"
email= "sidhrmiglani@gmail.com"
def send_email(request):
    if request.method == 'POST':
        form = SendEmailForm(request.POST)
        if form.is_valid():
            global staff_id
            global first_name
            global last_name
            global email
            staff_id = form.cleaned_data.get('staff_id')
            url="https://gibice-hrserver.herokuapp.com/info/"+staff_id
            req = urllib.request.Request(url)
            r = urllib.request.urlopen(req).read()
            cont = json.loads(r.decode('utf-8'))
            first_name=cont['first_name']
            last_name = cont['last_name']
            email=cont['email']
            message = render_to_string('learner_account_activation_email.html', {
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(staff_id)),
                'token': account_activation_token.make_token(staff_id),
            })
            send_mail(
                'Activate your account',
                message,
                settings.EMAIL_HOST_USER,
                ['wa201801@163.com'],
            )
            return redirect('learners:waitforactivation')
    else:
        form =SendEmailForm()
    return render(request, 'learner_signup.html', {'form': form})

def waitforactivation(request):
    return render(request,'waitforactivation.html')

def activate(request, uidb64, token):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user=User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,
                                     email=email)
            learner=Learner.objects.create(username=username,password=password,first_name=first_name,last_name=last_name,
                                     email=email,staff_id=staff_id)
            my_group = Group.objects.get(name='learner')
            my_group.user_set.add(user)
            return redirect('learners:activate_complete')
    else:
        form = SignupForm()
    return render(request, 'learner_activate.html', {'form': form})

def activate_complete(request):
    return render(request, 'learner_activate_complete.html')

@login_required
@user_passes_test(is_member)
def user_center(request):
    return redirect('learners:active-course', category='all')

@login_required
@user_passes_test(is_member)
def active_course(request, category):
    learner = Learner.objects.get(username=request.user.username)
    learner_history = EnrollmentHistory.objects.filter(learner=learner)
    categories = Category.objects.all()
    if category == 'all':
        active_courses = Course.objects.all()
    else:
        active_courses = Course.objects.filter(category=category)

    course_and_status = []
    for course in active_courses:
        has_history = False
        status = ""
        for history in learner_history:
            if course == history.course and history.completed is True:
                status = "Completed"
                has_history = True
            elif course == history.course and history.completed is False:
                status = "Enrolled"
                has_history = True

        if has_history is False:
            status = "Enroll"
        course_and_status.append((course, status))
    print(course_and_status)

    return render(request, 'usercenter-activecourse.html', {'course_and_status': course_and_status,
                                                            'categories': categories
                                                            })

@login_required
@user_passes_test(is_member)
def enroll_course(request, course_id):
    learner = Learner.objects.get(username=request.user.username)
    course = Course.objects.get(id=course_id)
    history = EnrollmentHistory.objects.create(learner=learner, course=course, completed=False)
    history.save()
    progress = Progress.objects.create(learner=learner, course=course, latest_progress=1)
    progress.save()
    quiz_result = QuizResult.objects.create(learner=learner, course=course, total_score=0)
    quiz_result.save()
    modules = Module.objects.filter(Course_id = course_id)

    return render(request, 'learner_modules.html', {'course': course, 'modules': modules,
                                                    'progress': progress.latest_progress})



@login_required
def course_detail(request,course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'learner_course_detail.html', {'course': course})


@user_passes_test(is_member)
def modules(request,course_id):
    current_learner = Learner.objects.get(username=request.user.username)
    course = Course.objects.get(id=course_id)
    learner_progress = Progress.objects.get(learner=current_learner, course=course)
    modules = Module.objects.filter(Course_id=course.id).order_by('order')
    return render(request, 'learner_modules.html', {'course': course, 'modules': modules,
                                                    'progress': learner_progress.latest_progress})

@login_required
@user_passes_test(is_member)
def module_detail(request, moduleid): # TODO: Connect with a better URL
    username = request.user.username
    module = Module.objects.get(id=moduleid)
    current_course = module.Course
    progress = Progress.objects.get(learner__username=username, course=current_course)
    components = Component.objects.filter(Module_id=module.id).order_by('order')
    current_learner = Learner.objects.get(username=username)
    learner_progress = Progress.objects.get(learner=current_learner, course=current_course).latest_progress
    question_number = module.question_number
    if(question_number>0):
        QUESTION_CHOICES = [x.id for x in QuizQuestion.objects.filter(course_id=current_course.id, module_id=module.id)]
        for i in QUESTION_CHOICES:
            question = QuizQuestion.objects.get(id=i)
            question.selected = False
            question.save()
        questionids = random.sample(QUESTION_CHOICES, question_number)
        for i in questionids:
            question = QuizQuestion.objects.get(id=i)
            question.selected = True
            question.save()

    return render(request, 'learner_module_detail.html', {'components': components,'username':username, 'module': module, 'progress': progress.latest_progress})



@login_required
@user_passes_test(is_member)
@csrf_protect
def take_quiz(request, course_id, username):
    current_learner = Learner.objects.get(username=username)
    current_course = Course.objects.get(id=course_id)
    learner_progress = Progress.objects.get(learner=current_learner, course=current_course).latest_progress
    current_module = current_course.module_set.get(order=learner_progress)
    question_list = list(current_course.quizquestion_set.filter(selected=True, module_id=current_module.id))
    # question_list = list(current_course.quizquestion_set.filter(selected=True, id=current_module.id))
    if request.method == 'POST':
        form = QuizForm(request.POST or None, questions=question_list)
        total = 0

        if form.is_valid():
            # for (question_description, answer) in form.cleaned_data():
            choices = form.cleaned_data.values()
            for choice in choices:
                # choice = QuizChoice.objects.get(choice_text=answer)
                print(choice.choice_text)
                total += choice.value
                print(choice.value)
                quiz_result = QuizResult.objects.get(learner=current_learner, course=current_course)
                quiz_result.total_score = total
                quiz_result.save()
            QUESTION_CHOICES = [x.id for x in QuizQuestion.objects.filter(course_id=current_course.id, module_id=current_module.id)]
            for i in QUESTION_CHOICES:
                question = QuizQuestion.objects.get(id=i)
                question.selected = True
                question.save()
            return redirect('learners:view_result', course_id=course_id, username=username)
    else:
        form = QuizForm(questions=question_list)

    return render(request, 'take_quiz.html', {'form': form,
                                              'course_id': course_id,
                                              'username': username,
                                              })


@login_required
@user_passes_test(is_member)
def view_result(request, course_id, username):
    # Get learner, course, and progress
    current_learner = Learner.objects.get(username=username)
    current_course = Course.objects.get(id=course_id)
    learner_progress = Progress.objects.get(learner=current_learner, course=current_course)

    # Get module info
    print(current_course.module_set.all)
    current_module = current_course.module_set.filter(order=learner_progress.latest_progress)[0]

    # print(current_module.title)
    current_order = current_module.order

    # Is the learner taking the quiz of the last module?
    is_last_module = False
    next_module_id = 0
    if len(current_course.module_set.all()) == learner_progress.latest_progress: # Learner progress = number of modules in this course
        is_last_module = True
    else:
        next_module = Module.objects.get(Course_id=course_id, order=current_order + 1)
        next_module_id = next_module.id

    # Get quiz result (pass or fail)
    latest_submission = QuizResult.objects.get(learner=current_learner, course=current_course)
    if latest_submission.total_score >= current_module.pass_score: # TODO: How does instructor set the passing score?
        result = "passed"
        if is_last_module:
            time_now = datetime.datetime.now()
            update_learner_history(username, course_id, time_now)
            current_learner.CECU += current_course.CECU
            current_learner.save()
            message = render_to_string('learner_pass_course.html', {
                'learner':current_learner.first_name,
                 'course':current_course.title,
                 'CECU':current_course.CECU
            })
            send_mail(
                'You have completed course',
                message,
                settings.EMAIL_HOST_USER,
                [current_learner.email],
            )
        # else:
        learner_progress.latest_progress = learner_progress.latest_progress + 1
        learner_progress.save()
    else:
        result = 'failed'

    return render(request, 'quiz_result.html', {'total_score': latest_submission.total_score,
                                                'pass_or_fail': result,
                                                'current_module_id':current_module.id,
                                                'next_module_id': next_module_id,
                                                'is_last_module': is_last_module,
                                                })


def update_learner_history(username, course_id, time):
    current_learner = Learner.objects.get(username=username)
    current_course = Course.objects.get(id=course_id)
    learner_history = EnrollmentHistory.objects.get(learner=current_learner, course=current_course)
    learner_history.date_completed = time
    learner_history.completed = True
    learner_history.save()


def view_completed_course(request):
    learner = Learner.objects.get(username=request.user.username)
    learner_history = EnrollmentHistory.objects.filter(learner=learner, completed=True)
    course_taken = []
    cumulative_cecu = 0
    course_list = learner_history.order_by('date_completed')
    for i in range(len(course_list)):
        cumulative_cecu += course_list[i].course.CECU
        course_taken.append([course_list[i].course,
                             course_list[i].date_completed,
                             course_list[i].course.CECU,
                             cumulative_cecu])

    return render(request, 'completed_course.html', {'course_taken': course_taken})
