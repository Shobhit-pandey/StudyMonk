from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

CHOICE = (
    ('male', 'male'),
    ('female', 'female'),
    ('other','other')
)

class StudentRegistration(models.Model):
    user = models.ForeignKey(User)
    college_name = models.CharField(max_length=100)
    gender = models.CharField(choices=CHOICE,default='male', max_length=20)

    def __str__(self):
        return self.user.email


class FacultyRegistration(models.Model):
    user = models.ForeignKey(User)
    college_name = models.CharField(max_length=100)
    mentorship_status = models.BooleanField()
    description = models.CharField(max_length=1000)
    gender = models.CharField(choices=CHOICE, default='male', max_length=20)

    def __str__(self):
        return self.user.email