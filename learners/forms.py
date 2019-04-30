from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.db import transaction
from django.forms.utils import ValidationError

class SendEmailForm(forms.Form):
    staff_id= forms.CharField(max_length=30,help_text='Required. Inform your staff id.')
class SignupForm(forms.Form):
    username= forms.CharField(max_length=30,help_text='Required. Inform your username.')
    password = forms.CharField(max_length=30, help_text='Required. Inform your password.')
# class StudentSignUpForm(UserCreationForm):
#     staff_id = forms.CharField(max_length=100, help_text='Required. Inform your staff id.')
#     class Meta(UserCreationForm.Meta):
#         model = User
#
#     @transaction.atomic
#     def save(self):
#         user = super().save(commit=False)
#         user.is_student = True
#         user.save()
#         student = Learner.objects.create(user=user)
#         return user
