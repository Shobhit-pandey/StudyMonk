# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect,reverse

# Create your views here.
from mywebsite.form import StudentRegistrationForm, FacultyRegistrationForm

def home(request):
    return render(request,'mywebsite/home.html')

def about_us(request):
    return render(request,'mywebsite/about.html')

def discussion_forum(request):
    return render(request,'mywebsite/discussion_forum.html')

def student_signup(request):
    if (request.method=='POST'):
        form=StudentRegistrationForm(request.POST)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = StudentRegistrationForm()
    return render(request,'mywebsite/Studentsign.html',{'form':form})

def faculty_signup(request):
    if (request.method=='POST'):
        form=FacultyRegistrationForm(request.POST)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = FacultyRegistrationForm()
    return render(request,'mywebsite/Teachersign.html',{'form':form})