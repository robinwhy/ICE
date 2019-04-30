from django import forms
from courses import models
from django.core.files.uploadedfile import SimpleUploadedFile

class SendEmailForm(forms.Form):
    instructor_email = forms.CharField(max_length=50, help_text='Please input instructor email here.')

class SignupForm(forms.Form):
    username= forms.CharField(max_length=30,help_text='Required. Please input your username.')
    password = forms.CharField(max_length=30, help_text='Required. Inform input your password.')
    first_name = forms.CharField(max_length = 30, help_text = 'Required. Please input your first name')
    last_name = forms.CharField(max_length = 30, help_text = 'Required. Please input your last name')
    autobiography = forms.CharField(max_length = 2000, help_text = 'Required. Please input a short autobiography (2000 characters)')


class createCourse(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['title', 'description', 'thumb', 'category', 'CECU', 'category']

class createModule(forms.ModelForm):
    class Meta:
        model = models.Module
        fields = ['title', 'order']

class addComponent(forms.Form):
    def __init__(self, *args, **kwargs):
        # print(kwargs)
        self.courseid = kwargs.pop('courseid')
        # QUESTION_CHOICES = models.QuizQuestion.objects.filter(module_id=self.moduleid)
        COMPONENT_CHOICES = [[x.id, x.title] for x in models.Component.objects.filter(Course_id=self.courseid) if x.Module_id== None ]
        super(addComponent, self).__init__(*args, **kwargs)
        self.fields['components'] = forms.MultipleChoiceField(choices=COMPONENT_CHOICES, required=False,
                                                             widget=forms.CheckboxSelectMultiple())
        self.fields['order'] = forms.IntegerField(max_value=100,required = False, min_value = 1)

class reorderModule(forms.Form):
    def __init__(self, *args, **kwargs):
        # print(kwargs)
        self.courseid = kwargs.pop('courseid')
        # QUESTION_CHOICES = models.QuizQuestion.objects.filter(module_id=self.moduleid)
        MODULE_CHOICES = [[x.id, x.title] for x in models.Module.objects.filter(Course_id=self.courseid) ]
        super(reorderModule, self).__init__(*args, **kwargs)
        self.fields['module'] = forms.CharField(required=False,
                                                             widget=forms.Select(choices=MODULE_CHOICES))
        self.fields['order'] = forms.IntegerField(max_value=100,required = True, min_value = 1)

class reorderComponent(forms.Form):
    def __init__(self, *args, **kwargs):
        # print(kwargs)
        self.courseid = kwargs.pop('courseid')
        self.moduleid = kwargs.pop('moduleid')
        # QUESTION_CHOICES = models.QuizQuestion.objects.filter(module_id=self.moduleid)
        COMPONENT_CHOICES = [[x.id, x.title] for x in models.Component.objects.filter(Course_id=self.courseid, Module_id = self.moduleid) ]
        super(reorderComponent, self).__init__(*args, **kwargs)
        self.fields['components'] = forms.CharField(required=False,
                                                             widget=forms.Select(choices=COMPONENT_CHOICES))
        self.fields['order'] = forms.IntegerField(max_value=100,required = True, min_value = 1)

class createQuiz(forms.Form):
    def __init__(self, *args, **kwargs):
        # print(kwargs)
        self.courseid = kwargs.pop('courseid')
        # QUESTION_CHOICES = models.QuizQuestion.objects.filter(module_id=self.moduleid)
        QUESTION_CHOICES = [[x.id, x.question_text] for x in models.QuizQuestion.objects.filter(course_id=self.courseid) if x.selected==False ]
        super(createQuiz, self).__init__(*args, **kwargs)
        self.fields['questions'] = forms.MultipleChoiceField(choices=QUESTION_CHOICES, required=False,
                                                             widget=forms.CheckboxSelectMultiple())
        self.fields['pass_score'] = forms.IntegerField(min_value=0, max_value=100)
        self.fields['question_number'] = forms.IntegerField(min_value=0, max_value=10)
