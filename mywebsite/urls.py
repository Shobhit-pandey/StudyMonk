from django.conf.urls import url
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, \
    password_reset_complete
from django.views.generic import TemplateView

from mywebsite import views

urlpatterns = [
    url(r'^$',views.home,name='home'),
    url(r'^login/$',login,{'template_name':'student/Studentlogin.html'}, name='login' ),
    url(r'^discussion-forum/$',views.discussion_forum,name='discussion_forum'),
    url(r'^about-us/$',views.about_us,name='about_us'),
    url(r'^actual/$',views.actual,name='actual'),
    url(r'^colleges/$',views.colleges_list,name='college'),
    url(r'^courses/$',views.courses_list,name='course'),
    url(r'^accounts/student/signup/$', views.student_signup, name='student_signup'),
    url(r'^accounts/student/edit/$', views.student_edit, name='student_edit'),
    url(r'^accounts/faculty/edit/$', views.faculty_edit, name='faculty_edit'),
    url(r'^accounts/student/password/$', views.change_password, name='change_password'),
    url(r'^accounts/faculty/password/$', views.change_password, name='change_password'),
    url(r'^accounts/faculty/signup/$', views.faculty_signup, name='faculty_signup'),
    url(r'^accounts/profile/$', views.profile, name='profile'),
    url(r'^accounts/logout/$', logout,{'template_name':'mywebsite/home.html'}, name='logout'),
    url(r'^accounts/student/login/$', login,{'template_name':'student/Studentlogin.html'}, name='student_login'),
    url(r'^accounts/faculty/login/$',login,{'template_name':'faculty/Teacherlogin.html'}, name='faculty_login'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^college-list/(?P<pk1>[\w\-]+)/$', views.college_detail, name='college_detail'),
    url(r'^faculty/topic/add/$', views.topic_upload, name='topic_upload'),
    url(r'^upload/(?P<pk6>[\w\-]+)/$', views.personal_upload, name='personal_upload'),
    url(r'^faculty/upload/(?P<pk5>[\w\-]+)/$', views.faculty_upload, name='faculty_upload'),
    url(r'^college/courses/faculty-list/(?P<pk3>[\w\-]+)/$', views.faculty_college, name='faculty_college'),
    url(r'^courses/college/faculty-list/(?P<pk4>[\w\-]+)/$', views.faculty_course, name='faculty_course'),
    url(r'^course-list/(?P<pk2>[\w\-]+)/$', views.course_detail, name='course_detail'),
    url(r'^doc/add/(?P<pk7>[\w\-]+)/$', views.add_doc, name='add_doc'),
    url(r'^comment/profile/(?P<pk10>[\w\-]+)/$', views.commentprofile, name='commentprofile'),
    url(r'^account/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^accounts/reset-password/$',password_reset,{'template_name':'accounts/reset_password.html',
                                             'post_reset_redirect':'mywebsite:password_reset_done',
                                             'email_template_name':'accounts/reset_password_email.html'},name='reset_password'),

    url(r'^accounts/reset-password/done/$',password_reset_done,{'template_name':'accounts/reset_password_done.html'},name='password_reset_done'),


    url(r'^accounts/reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',password_reset_confirm,name='password_reset_confirm'),
    url(r'^accounts/reset-password/complete/$',password_reset_complete,name='password_reset_complete'),
    url(r'^QuestionList/$', views.SubjectList.as_view(), name='question-list'),
    url(r'^questions/(?P<pk>\d+)/$',views.questions, name='questions'),
    url(r'^comments/(?P<pk>\d+)/$',views.discussioncomments, name='comments'),
    url(r'^comment/$',views.discussioncomment, name='comment'),
    url(r'^answers/$',TemplateView.as_view(template_name='ans.html'), name='answers' ),
    url(r'^add_q/(?P<pk>\d+)/$',views.fill_question, name='add-q' ),
    url(r'^comment/add/(?P<pk9>[\w\-]+)/$', views.add_comment, name='add_comment'),
    url(r'^video/add/(?P<pk8>[\w\-]+)/$', views.add_video, name='add_video'),
    ]