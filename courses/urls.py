from django.conf.urls import url
from . import views

app_name = 'courses'

urlpatterns = [
    url(r'^instructor$', views.instructor_course_list, name="list"),
]