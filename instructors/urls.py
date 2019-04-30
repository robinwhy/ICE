from django.conf.urls import url
from . import views

app_name = 'instructors'

urlpatterns = [
    url(r'^$', views.instructor_course_list, name="list"),

    url(r'^signup$', views.send_email, name ="send_email"),
    url(r'^waitforactivation$', views.waitforactivation, name="waitforactivation"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^activatecomplete', views.activate_complete, name="activate_complete"),

    url(r'^modules/(?P<course_id>[\w-]+)/$', views.instructor_modules, name="instructor-modules"),

    url(r'^modules/addcourse$', views.add_course, name="instructor-add-course"),
    url(r'^modules/addmodule/(?P<courseid>[\w-]+)/$', views.add_module, name="instructor-add-module"),
    url(r'^module-detail/module(?P<moduleid>[\w-]+)/$', views.instructor_components, name="instructor-module-detail"),
    url(r'^modules/(?P<moduleid>[\w-]+)/addcomponent/$', views.add_component, name="instructor-add-component"),
    url(r'^modules/(?P<moduleid>[\w-]+)/reordercomponent/$', views.reorder_component, name="instructor-reorder-component"),
    url(r'^modules/(?P<courseid>[\w-]+)/reordermodule/$', views.reorder_module, name="instructor-reorder-module"),
    url(r'^modules/(?P<moduleid>[\w-]+)/addquiz/$', views.add_quiz, name="instructor-add-quiz"),
    url(r'^modules/(?P<moduleid>[\w-]+)/viewquiz/$', views.instructor_view_quiz, name="instructor-view-quiz"),
]
