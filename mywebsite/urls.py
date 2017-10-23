from django.conf.urls import url
from django.contrib.auth.views import login

from mywebsite import views

urlpatterns = [
    url(r'^$',views.home,name='home'),
    url(r'^discussion-forum/$',views.discussion_forum,name='discussion_forum'),
    url(r'^about-us/$',views.about_us,name='about_us'),
    url(r'^accounts/student/signup/$', views.student_signup, name='student_signup'),
    url(r'^accounts/faculty/signup/$', views.faculty_signup, name='faculty_signup'),
    url(r'^accounts/student/login/$', login,{'template_name':'mywebsite/Studentlogin.html'}, name='student_login'),
    url(r'^accounts/faculty/login/$', login,{'template_name':'mywebsite/Teacherlogin.html'}, name='faculty_login'),

    ]