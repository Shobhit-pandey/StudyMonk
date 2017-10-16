# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect ,reverse

# Create your views here.
def home(request):
    return render(request,'mywebsite/home.html')