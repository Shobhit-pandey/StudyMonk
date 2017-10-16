# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect ,reverse

# Create your views here.
def home(request):
    return render(request,'mywebsite/home.html')

def about_us(request):
    return render(request,'mywebsite/about.html')

def discussion_forum(request):
    return render(request,'mywebsite/discussion_forum.html')