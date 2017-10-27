# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404

# Create your views here.
from mywebsite.form import StudentRegistrationForm, FacultyRegistrationForm
from mywebsite.models import StudentRegistration, FacultyRegistration


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
        print("student")
        form=StudentRegistrationForm(request.POST)
        if (form.is_valid()):
            print("valid")
            form.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = StudentRegistrationForm()
    return render(request, 'student/Studentsign.html', {'form':form})

def faculty_signup(request):
    if (request.method=='POST'):
        form=FacultyRegistrationForm(request.POST)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect(reverse('home'))
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
            Profile = form.save(commit=False)
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
            Profile = form.save(commit=False)
            Profile.user=request.user
            Profile.save()
            form.save()
            return redirect(reverse('home'),pk=Profile.pk)
    else:
        form=StudentRegistrationForm(instance=Profile)
        args={'form':form}
        return render(request,'faculty/edit_teacher.html',args)