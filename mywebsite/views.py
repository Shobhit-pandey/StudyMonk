# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import smtplib

from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
# Create your views here.
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import generic
from tzlocal import get_localzone

from mywebsite.form import StudentRegistrationForm, FacultyRegistrationForm, StudentEditProfile, FacultyEditProfile, \
    TopicForm, DocumentForm, VideoForm, CommentForm, DiscussionCommentForm, QForm, QuestionForm
from mywebsite.models import StudentRegistration, FacultyRegistration, CollegeName, CourseName, AboutUs, CollegeCourses, \
    Topic, TopicThread, DiscussionComment, Subject, Thread
from mywebsite.token import account_activation_token


def user_login(request):
    pass

def home(request):
    return render(request,'mywebsite/home.html')

@login_required()
def profile(request):
    user_id = request.user.id
    try :
        person = StudentRegistration.objects.filter(user_id=user_id).get()
    except:
        person = FacultyRegistration.objects.filter(user_id=user_id).get()
    return render(request,'mywebsite/Profile.html',{'person':person})

def actual(request):
    return render(request,'mywebsite/actual.html')

def about_us(request):
    about_us = AboutUs.objects.all()
    return render(request,'mywebsite/about.html',{'about_us':about_us})

def discussion_forum(request):
    return render(request,'mywebsite/discussion_forum.html')
def colleges_list(request):
    college = CollegeName.objects.all()
    return render(request, 'mywebsite/collegeslist.html', {'college':college})
def courses_list(request):
    course = CourseName.objects.all()
    return render(request, 'mywebsite/courses.html', {'course':course})

def student_signup(request):
    college = CollegeName.objects.all()
    if (request.method=='POST'):
        form=StudentRegistrationForm(request.POST)
        if (form.is_valid()):
            user = form.save()
            user.is_active=False
            user.is_staff=False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate StudyMonk Student Account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # user.email_user(subject, message)
            send_verification_mail(user.email,message)
            return redirect('mywebsite:account_activation_sent')
            #return redirect('home')
            #return HttpResponseRedirect(reverse('home'))
    else:
        form = StudentRegistrationForm()
    return render(request, 'student/Studentsign.html', {'form':form})

def faculty_signup(request):
    college = CollegeName.objects.all()
    course = CourseName.objects.all()
    form = FacultyRegistrationForm()
    if (request.method=='POST'):
        college = CollegeName.objects.all()
        course = CourseName.objects.all()
        # print college.college_name
        form=FacultyRegistrationForm(request.POST)
        if (form.is_valid()):
            user = form.save()
            user.is_active = False
            user.is_staff=True
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate StudyMonk Faculty Account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_verification_mail(user.email, message)
            return redirect('mywebsite:account_activation_sent')
            #return HttpResponseRedirect(reverse('home'))
    else:
        form = FacultyRegistrationForm()
    return render(request, 'faculty/Teachersign.html', {'form':form,'college':college,'course':course})

@login_required
def change_password(request):
    if request.method=='POST':
        form=PasswordChangeForm(data=request.POST,user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect(reverse('mywebsite:home'))
        else:
            return redirect(reverse('mywebsite:change_password'))
    else:
        form=PasswordChangeForm(user=request.user)
        user_id = request.user.id
        try:
            person = StudentRegistration.objects.filter(user_id=user_id).get()
            print (person.user.email)
        except:
            person = FacultyRegistration.objects.filter(user_id=user_id).get()
            print (person.user.email)
        args={'form':form,'person':person}
        return render(request,'accounts/edit_password.html',args)

@login_required()
def student_edit(request):
    user_id = request.user.id
    try:
        person = StudentRegistration.objects.filter(user_id=user_id).get()
    except:
        person = FacultyRegistration.objects.filter(user_id=user_id).get()
    if request.method=='POST':
        form=StudentEditProfile(request.POST,instance=request.user)

        # if form.is_valid():
        form.save()
        return redirect(reverse('mywebsite:home'))
    else:
        form=StudentEditProfile(instance=request.user)
    return render(request, 'student/edit_student.html', {'form': form, 'person': person})


@login_required()
def faculty_edit(request):
    user_id = request.user.id
    try:
        person = StudentRegistration.objects.filter(user_id=user_id).get()
    except:
        person = FacultyRegistration.objects.filter(user_id=user_id).get()
    if request.method=='POST':
        form=FacultyEditProfile(request.POST,instance=request.user)

        # if form.is_valid():
        form.save()
        return redirect(reverse('mywebsite:home'))
    else:
        form=FacultyEditProfile(instance=request.user)
    return render(request, 'faculty/edit_teacher.html', {'form': form, 'person': person})


def account_activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('mywebsite:home')
    else:
        return render(request, 'accounts/account_activation_invalid.html')

email_address = 'studymonk.se@gmail.com'
email_password = 'qwertyuiopzxcvbnm'


def send_verification_mail(email, msg):
    print("send verificaion mail")
    try:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.set_debuglevel(1)
        server.starttls()
        server.ehlo()
        server.login('studymonk.se@gmail.com', 'qwertyuiopzxcvbnm')
        server.sendmail(email_address, email, msg)
        server.quit()
        print('successfully sent the mail')
    except:
        print("failed to send mail")

def college_detail(request,pk1):
    college = get_object_or_404(CollegeName,pk=pk1)
    college_id = pk1
    college_name = CollegeCourses.objects.filter(college_id_id=college_id)
    course_name = CourseName.objects.all()

    return render(request, 'mywebsite/collegetocourses.html', {'college':college,'college_name':college_name,
                                                               'course_name':course_name})

def course_detail(request,pk2):
    course = get_object_or_404(CourseName,pk=pk2)
    course_id = pk2
    course_name = CollegeCourses.objects.filter(course_id_id=course_id)
    college_name = CollegeName.objects.all()

    return render(request, 'mywebsite/coursetocolleges.html', {'course':course,'course_name':course_name,
                                                               'college_name':college_name})

def faculty_college(request,pk3):
    referer = request.META.get('HTTP_REFERER')
    faculty = get_object_or_404(CourseName,pk=pk3)
    course_id = pk3
    college_id = referer[-2]
    print(college_id)
    faculty_name = FacultyRegistration.objects.filter(course_name_id=course_id)
    faculty_college_name = FacultyRegistration.objects.filter(college_name_id=college_id)
    #college_name = CollegeName.objects.all()

    return render(request, 'mywebsite/facultyfromcollege.html', {'faculty':faculty,'faculty_name':faculty_name,
                                                                 'faculty_college_name':faculty_college_name
                                                               })
def faculty_course(request,pk4):
    referer = request.META.get('HTTP_REFERER')
    faculty = get_object_or_404(CollegeName,pk=pk4)
    college_id = pk4
    course_id = referer[-2]
    print(college_id)
    faculty_name = FacultyRegistration.objects.filter(college_name_id=college_id)
    faculty_course_name = FacultyRegistration.objects.filter(course_name_id=course_id)
    #college_name = CollegeName.objects.all()

    return render(request, 'mywebsite/facultyfromcourses.html', {'faculty':faculty,'faculty_name':faculty_name,
                                                                 'faculty_course_name':faculty_course_name
                                                               })
@login_required()
def faculty_upload(request,pk5):
    faculty = get_object_or_404(FacultyRegistration,pk=pk5)
    upload = pk5
    faculty_name = FacultyRegistration.objects.filter(id=upload)
    topic = Topic.objects.all()
    topic_thread = TopicThread.objects.all();
    return render(request, 'mywebsite/faculty_upload.html', {'faculty':faculty,'faculty_name':faculty_name,
                                                                 'topic':topic,'topic_thread':topic_thread
                                                               })
@login_required()
def topic_upload(request):
    if request.method=='POST':
        form = TopicForm(request.POST,initial={'user_id':request.user.id})
        if form.is_valid():
            # u =form.save(commit=False)
            # u.user_id=request.user.id
            # u.save()
            # # form.save().user_id=request.user.id
            form.save()
            return redirect('mywebsite:home')
    else:
        form = TopicForm(initial={'user_id':request.user.id})

    return render(request, 'mywebsite/topic_create.html',{'form':form})

@login_required()
def personal_upload(request,pk6):
    faculty = get_object_or_404(User,pk=pk6)
    upload=pk6
    topic_name = Topic.objects.filter(user_id=upload)
    return render(request,'mywebsite/personal_upload.html',{'faculty':faculty,'topic_name':topic_name})

@login_required()
def add_doc(request,pk7):
    topic = get_object_or_404(Topic, pk=pk7)
    form = DocumentForm(initial={'topic_id': pk7})
    if request.method=='POST':
        form = DocumentForm(request.POST,request.FILES,initial={'topic_id':pk7})
        if form.is_valid():
            form.save()
            return redirect('mywebsite:home')
    else:
        form = DocumentForm(initial={'topic_id':pk7})

    return render(request, 'mywebsite/add_doc.html',{'form':form,'topic':topic})

@login_required()
def add_video(request,pk8):
    topic = get_object_or_404(Topic,pk=pk8)
    form = VideoForm(initial={'topic_id': pk8})
    if request.method=='POST':
        form = VideoForm(request.POST,request.FILES,initial={'topic_id':pk8})
        if form.is_valid():
            form.save()
            return redirect('mywebsite:home')
    else:
        form = VideoForm(initial={'topic_id':pk8})

    return render(request, 'mywebsite/add_video.html',{'form':form,'topic':topic})

@login_required()
def add_comment(request,pk9):
    topic = get_object_or_404(Topic,pk=pk9)
    if request.method == 'POST':
        local_tz = get_localzone()
        timezone.activate(local_tz)
        form =CommentForm(request.POST,initial={'topic_id':pk9,'user_id':request.user.id,'time_stamp':datetime.datetime.now()})
        if form.is_valid():
            form.save()
            return redirect('mywebsite:home')
    else:
        form = CommentForm(initial={'topic_id': pk9, 'user_id': request.user.id,
                                                  'time_stamp': datetime.datetime.now()})
    return render(request, 'mywebsite/add_comment.html', {'form': form, 'topic': topic})

@login_required()
def faculty_comments(request,pk10):
    topic = get_object_or_404(Topic,pk=pk10)
    if request.method == 'POST':
        form =CommentForm(request.POST,initial={'topic_id':pk10,'user_id':request.user.id,'time_stamp':datetime.datetime.now()})
        if form.is_valid():
            form.save()
            return redirect('mywebsite:home')
        else:
            form = CommentForm(initial={'topic_id': pk10, 'user_id': request.user.id,
                                                      'time_stamp': datetime.datetime.now()})
        return render(request, 'mywebsite/personal_upload.html', {'form': form, 'topic': topic})


# Create your views here.

def discussioncomment(request):
    if request.method == 'POST':
        comment_form = DiscussionCommentForm(request.POST)
        pk1 = request.POST['pk']
        if comment_form.is_valid():

            # pk1 = Thread.pk
            com = comment_form.save()
            com.save()
            lists = DiscussionComment.objects.filter(thread=pk1)
            args = {'lists': lists}
            return render(request, 'mywebsite/ans.html', args)

        else:
            print (comment_form.errors)
            return HttpResponseRedirect(reverse('mywebsite:question-list'))

    else:
        comment_form = DiscussionCommentForm()
        return render(request, 'mywebsite/ques.html', {'comment_form': comment_form})


class SubjectList(generic.ListView):
    model = Subject
    template_name = 'mywebsite/QuestionList.html'
    context_object_name = 'subs'

    def get_queryset(self):
        return Subject.objects.all()


def questions(request, pk):
    global answers
    ques = Thread.objects.filter(subject=pk)
    var = ""
    for q in ques:
        var = q.subject

    return render(request, 'mywebsite/ques.html', {'ques': ques, 'var': var, 'pk': pk})


class DiscussionCommentComment(object):
    pass


def discussioncomments(request, pk):
    lists = DiscussionComment.objects.filter(thread=pk)
    args = {'lists': lists}
    return render(request, 'mywebsite/ans.html', args)


def fill_question(request, pk):
    if request.method == 'POST':

        q_form = QForm(request.POST)

        if q_form.is_valid():
            # ques = Thread.objects.filter(subject=pk)

            q_question = q_form['question'].value()
            q_user = request.user
            q_subject = Subject.objects.get(pk=pk)
            T = Thread.objects.create(question=q_question, subject=q_subject, user=q_user)
            T.save()
            print(T)
            ques = Thread.objects.filter(subject=pk)
            return render(request, 'mywebsite/ques.html', {'ques':ques,'pk':pk})


        else:
            print(QForm.errors)
            return HttpResponseRedirect(reverse('mywebsite:student_login'))

    else:
        q_form = QuestionForm()
        return render(request, 'mywebsite/add_question.html', {'q_form': q_form})


