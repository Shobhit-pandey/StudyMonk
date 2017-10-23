# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect ,reverse

# Create your views here.
from mywebsite.form import StudentRegistration, FacultyRegistration


def home(request):
    return render(request,'mywebsite/home.html')

def about_us(request):
    return render(request,'mywebsite/about.html')

def discussion_forum(request):
    return render(request,'mywebsite/discussion_forum.html')

def student_signup(request):
    if (request.method=='POST'):
        form=StudentRegistration(request.POST)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = StudentRegistration()
        args = {'form':form}
    return render(request,'mywebsite/Studentsign.html',{'form':form})

def faculty_signup(request):
    if (request.method=='POST'):
        form=FacultyRegistration(request.POST)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = FacultyRegistration()
        args = {'form':form}
    return render(request,'mywebsite/Teachersign.html',{'form':form})