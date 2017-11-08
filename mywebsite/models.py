from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

CHOICE = (
    ('male', 'male'),
    ('female', 'female'),
    ('other','other')
)
COPYRIGHT = (
    ('yes','yes'),
    ('no','no')
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


class AboutUs(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(choices=CHOICE,default='male',max_length=100)
    email = models.EmailField(null=False)
    fb_id = models.CharField(max_length=1000)
    github = models.CharField(max_length=1000)
    linkedin = models.CharField(max_length=1000)
    description = models.CharField(max_length=10000,null=False)
    dp = models.ImageField()

    def __str__(self):
        return self.email


class CollegeName(models.Model):
    college_name = models.CharField(max_length=200,primary_key=True)
    college_images = models.ImageField()

    def __str__(self):
        return self.college_name

class CourseName(models.Model):
    college_name = models.ForeignKey(CollegeName,null=False)
    course_name = models.CharField(max_length=200,primary_key=True)

    def __str__(self):
        return self.course_name


class Teaches(models.Model):
    faculty_id =models.ForeignKey(FacultyRegistration,null=False,unique=True)
    course_id = models.ForeignKey(CourseName,null=False,unique=True)
    class Meta:
        unique_together = (("course_id","faculty_id"),)

    def __str__(self):
        return self.faculty_id

class CollegeCourses(models.Model):
    course_id = models.ForeignKey(CourseName,null=False,unique=True)
    college_id = models.ForeignKey(CollegeName,null=False,unique=True)

    class Meta:
        unique_together = (("course_id","college_id"),)

    def __str__(self):
        return self.college_id

class Topic(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    course_id = models.ForeignKey(CourseName,null=False)

    def __str__(self):
        return self.title

class Upload(models.Model):
    faculty_id = models.ForeignKey(FacultyRegistration,unique=True)
    topic_id = models.ForeignKey(Topic,unique=True)
    time_stamp = models.TimeField(null=False)
    class Meta:
        unique_together = (("topic_id","faculty_id"),)
    def __str__(self):
        return self.faculty_id

class Document(models.Model):
    document_name = models.CharField(max_length=100)
    topic_id = models.ForeignKey(Topic)
    copyright = models.CharField(choices=COPYRIGHT,max_length=10)
    document_file = models.FileField()

    def __str__(self):
        return self.document_name

class Video(models.Model):
    video_name = models.CharField(max_length=100)
    topic_id = models.ForeignKey(Topic)
    copyright = models.CharField(choices=COPYRIGHT,max_length=10)
    video_file = models.FileField()

    def __str__(self):
        return self.video_name

class TopicThread(models.Model):
    questions = models.CharField(max_length=2000)
    topic_id = models.ForeignKey(Topic)
    time_stamp = models.TimeField()
    student_id = models.ForeignKey(StudentRegistration)

    def __str__(self):
        return self.questions

class StudentTopicComment(models.Model):
    content = models.CharField(max_length=10000)
    time_stamp = models.TimeField()
    thread_id = models.ForeignKey(TopicThread)
    student_id = models.ForeignKey(StudentRegistration)

    def __str__(self):
        return self.content

class FacultyTopicComment(models.Model):
    content = models.CharField(max_length=10000)
    time_stamp = models.TimeField()
    thread_id = models.ForeignKey(TopicThread)
    faculty_id = models.ForeignKey(FacultyRegistration)

    def __str__(self):
        return self.content

class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    def __str__(self):
        return self.subject_name

class Thread(models.Model):
    question = models.CharField(max_length=1000)
    subject_id = models.ForeignKey(Subject)
    time_stamp = models.TimeField
    student_id = models.ForeignKey(StudentRegistration)
    def __str__(self):
        return self.question

class StudentComment(models.Model):
    content = models.CharField(max_length=10000)
    time_stamp = models.TimeField()
    thread_id = models.ForeignKey(TopicThread)
    student_id = models.ForeignKey(StudentRegistration)

    def __str__(self):
        return self.content
class FacultyComment(models.Model):
    content = models.CharField(max_length=10000)
    time_stamp = models.TimeField()
    thread_id = models.ForeignKey(TopicThread)
    faculty_id = models.ForeignKey(FacultyRegistration)

    def __str__(self):
        return self.content