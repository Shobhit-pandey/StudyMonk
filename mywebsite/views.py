# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'mywebsite/home.html',{})

def discussion_forum(request):
    return render(request,'mywebsite/discussion_forum.html',{})

def about_us(request):
    return render(request,'mywebsite/about.html',{})

def Studentsign(request):
    return render(request,'mywebsite/Studentsign.html',{})
def Teachersign(request):
    return render(request,'mywebsite/Teachersign.html',{})
def Studentlogin(request):
    return  render(request,'mywebsite/Studentlogin.html',{})
def Teacherlogin(request):
    return  render(request,'mywebsite/Teacherlogin.html',{})

