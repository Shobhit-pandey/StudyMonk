from django.conf.urls import url
from mywebsite.views import home,discussion_forum,about_us,Studentsign

urlpatterns = [
    url(r'^$',home),
    url(r'^discussion-forum/',view=discussion_forum,name='discussion_forum'),
    url(r'^about-us',view=about_us,name='about_us'),
    url(r'^Student-sign/',view=Studentsign,name='studentsign'),

    ]