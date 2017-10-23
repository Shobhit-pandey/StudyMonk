from django.conf.urls import url

from mywebsite import views

urlpatterns = [
    url(r'^$',views.home,name='home'),
    url(r'^discussion-forum/$',views.discussion_forum,name='discussion_forum'),
    url(r'^about-us/$',views.about_us,name='about_us'),
    url(r'^accounts/student-signup/$', views.student_signup, name='student_signup'),

    ]