from django.conf.urls import url
from mywebsite.views import home,discussion_forum,about_us,Studentsign,Teachersign,Studentlogin,Teacherlogin

urlpatterns = [
    url(r'^$',home),
    url(r'^discussion-forum/',view=discussion_forum,name='discussion_forum'),
    url(r'^about-us',view=about_us,name='about_us'),
    url(r'^Student-sign/',view=Studentsign,name='studentsign'),
    url(r'^Teacher-sign/',view=Teachersign,name='teachersign'),
    url(r'^Student-login/',view=Studentlogin,name='studentlogin'),
    url(r'^Teacher-login/',view=Teacherlogin,name='teacherlogin'),


    ]