from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

CHOICE = (
    ('male', 'male'),
    ('female', 'female'),
    ('other','other')
)

class StudentRegistration(models.Model):
    user = models.ForeignKey(User,null=False)
    college_name = models.CharField(max_length=100,null=False)
    gender = models.CharField(choices=CHOICE,default='male', max_length=20,null=False)

    def __str__(self):
        return self.user.username


class FacultyRegistration(models.Model):
    user = models.ForeignKey(User,null=False)
    college_name = models.CharField(max_length=100,null=False)
    mentorship_status = models.BooleanField()
    description = models.CharField(max_length=1000,null=True)
    gender = models.CharField(choices=CHOICE, default='male', max_length=20,null=False)

    def __str__(self):
        return self.user.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    # other fields...

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()