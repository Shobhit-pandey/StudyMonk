# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from mywebsite.form import StudentRegistrationForm, FacultyRegistrationForm
from mywebsite.models import StudentRegistration, FacultyRegistration
from mywebsite.token import account_activation_token


def user_login(request):
    pass

def home(request):
    return render(request,'mywebsite/home.html')

def profile(request):
    return render(request,'mywebsite/home.html')

def about_us(request):
    return render(request,'mywebsite/about.html')

def discussion_forum(request):
    return render(request,'mywebsite/discussion_forum.html')

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
            return redirect('account_activation_sent')
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
            print("form save")
            user.is_active = False
            print("active")
            user.is_staff=True
            print("staff")
            user.save()
            print("save")
            current_site = get_current_site(request)
            subject = 'Activate StudyMonk Faculty Account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
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
            return redirect(reverse('home'))
        else:
            return redirect(reverse('change_password'))
    else:
        form=PasswordChangeForm(user=request.user)
        args={'form':form}
        return render(request,'accounts/edit_password.html',args)

@login_required()
def student_edit(request,pk):
    Profile = get_object_or_404(StudentRegistration,pk=pk)
    if request.method=='POST':
        form = StudentRegistrationForm(request.POST,instance=Profile)
        if form.is_valid():
            Profile = form.save()
            Profile.user=request.user
            Profile.save()
            form.save()
            return redirect(reverse('home'),pk=Profile.pk)
    else:
        form=StudentRegistrationForm(instance=Profile)
        args={'form':form}
        return render(request,'student/edit_student.html',args)


@login_required()
def faculty_edit(request,pk):
    Profile = get_object_or_404(FacultyRegistration,pk=pk)
    if request.method=='POST':
        form = FacultyRegistrationForm(request.POST,instance=Profile)
        if form.is_valid():
            Profile = form.save()
            Profile.user=request.user
            Profile.save()
            form.save()
            return redirect(reverse('home'),pk=Profile.pk)
    else:
        form=StudentRegistrationForm(instance=Profile)
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
        return redirect('home')
    else:
        return render(request, 'accounts/account_activation_invalid.html')