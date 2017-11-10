# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import update_session_auth_hash, authenticate, login, get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from mywebsite.form import StudentRegistrationForm, FacultyRegistrationForm, StudentEditProfile, FacultyEditProfile, \
    CollegeNameForm, CourseNameForm
from mywebsite.models import StudentRegistration, FacultyRegistration, CollegeName, CourseName, AboutUs
from mywebsite.token import account_activation_token


def user_login(request):
    pass

def home(request):
    return render(request,'mywebsite/home.html')

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
            user.email_user(subject, message)
            return redirect('mywebsite:account_activation_sent')
            #return redirect('home')
            #return HttpResponseRedirect(reverse('home'))
    else:
        form = StudentRegistrationForm()
    return render(request, 'student/Studentsign.html', {'form':form})

def faculty_signup(request):
    if (request.method=='POST'):
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
            user.email_user(subject, message)
            return redirect('mywebsite:account_activation_sent')
            #return HttpResponseRedirect(reverse('home'))
    else:
        form = FacultyRegistrationForm()
    return render(request, 'faculty/Teachersign.html', {'form':form})

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
    if request.method=='POST':
        form=StudentEditProfile(request.POST,instance=request.user)

        # if form.is_valid():
        form.save()
        return redirect(reverse('mywebsite:home'))
    else:
        form=StudentEditProfile(instance=request.user)
        args={'form':form}
        return render(request,'student/edit_student.html',args)


@login_required()
def faculty_edit(request):
    if request.method=='POST':
        form=FacultyEditProfile(request.POST,instance=request.user)

        # if form.is_valid():
        form.save()
        return redirect(reverse('mywebsite:home'))
    else:
        form=FacultyEditProfile(instance=request.user)
        args={'form':form}
        return render(request,'faculty/edit_teacher.html',args)


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