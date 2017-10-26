from django.conf.urls import url
from django.contrib.auth.views import login, logout

from mywebsite import views

urlpatterns = [
    url(r'^$',views.home,name='home'),
    url(r'^discussion-forum/$',views.discussion_forum,name='discussion_forum'),
    url(r'^about-us/$',views.about_us,name='about_us'),
    url(r'^accounts/student/signup/$', views.student_signup, name='student_signup'),
    url(r'^accounts/change-password/$', views.change_password, name='change_password'),
    url(r'^accounts/faculty/signup/$', views.faculty_signup, name='faculty_signup'),
    url(r'^accounts/profile/$', views.profile, name='profile'),
    url(r'^accounts/logout/$', logout,{'template_name':'mywebsite/home.html'}, name='logout'),
    url(r'^accounts/student/login/$', login,{'template_name':'accounts/Studentlogin.html'}, name='student_login'),
    url(r'^accounts/faculty/login/$', login,{'template_name':'accounts/Teacherlogin.html'}, name='faculty_login'),

    ]