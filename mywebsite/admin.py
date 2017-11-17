# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from mywebsite.models import Thread, Subject, FacultyTopicComment, StudentTopicComment, \
    TopicThread, Video, Document, Upload, Topic, CollegeCourses, Teaches, CourseName, CollegeName, AboutUs, Profile, \
    FacultyRegistration, StudentRegistration, Comment

admin.site.site_header = "Study Monk"

admin.site.register(StudentRegistration)
admin.site.register(FacultyRegistration)
admin.site.register(Profile)
admin.site.register(AboutUs)
admin.site.register(CollegeName)
admin.site.register(CourseName)
admin.site.register(Teaches)
admin.site.register(CollegeCourses)
admin.site.register(Topic)
admin.site.register(Upload)
admin.site.register(Document)
admin.site.register(Video)
admin.site.register(TopicThread)
admin.site.register(StudentTopicComment)
admin.site.register(FacultyTopicComment)
admin.site.register(Subject)
admin.site.register(Thread)
admin.site.register(Comment)

