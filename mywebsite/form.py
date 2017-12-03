from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from mywebsite.models import StudentRegistration, FacultyRegistration, AboutUs, CollegeName, CourseName, Topic, \
    Document, Video, Comment, Thread, DiscussionComment

CHOICE = (
    ('male', 'male'),
    ('female', 'female'),
    ('other','other')
)
COPYRIGHT = (
    ('no','no'),
    ('yes','yes'),
)

class StudentRegistrationForm(forms.Form):

    #TODO provide required attribute
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(required=True, max_length=100,widget=forms.PasswordInput)  # TODO (make password type input)
    first_name = forms.CharField(max_length=50,required=True)
    last_name = forms.CharField(max_length=50,required=True)
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(CHOICE,required=True)
    college_name = forms.ModelChoiceField(queryset=CollegeName.objects.all())

    def clean_password(self):
        MIN_LENGTH = 8
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("The new password must be at least 8 characters long.")
        return self.cleaned_data.get('password')

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data.get('email', None)).count() > 0:
            raise forms.ValidationError("User with this email already exists")

        req = ".ac.in"
        if req not in self.cleaned_data.get('email'):
            raise forms.ValidationError("sign up with your college account")

        return self.cleaned_data.get('email')

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data.get('username', None)).count() > 0:
            raise forms.ValidationError("User with this username already exists")

        return self.cleaned_data.get('username')

    def save(self, kwargs=None):
        print(self.cleaned_data)
        u = User.objects.create_user(first_name=self.cleaned_data.get('first_name'),
                                     last_name=self.cleaned_data.get('last_name'),
                                     email=self.cleaned_data.get('email'),
                                     password = self.cleaned_data.get('password'),
                                     username = self.cleaned_data.get('username'))
        u.save()

        s = StudentRegistration.objects.create(user=u,
                                               gender=self.cleaned_data.get('gender'),
                                               college_name = self.cleaned_data.get('college_name'))
        s.save()
        return u
    def clean_gender(self):
        print("clean gender: ", self.cleaned_data)
        return self.cleaned_data.get('gender')

class FacultyRegistrationForm(forms.Form):

    #TODO provide required attribute
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(required=True, max_length=100,widget=forms.PasswordInput)  # TODO (make password type input)
    first_name = forms.CharField(max_length=50,required=True)
    last_name = forms.CharField(max_length=50,required=True)
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(CHOICE,required=True)
    college_name = forms.ModelChoiceField(queryset=CollegeName.objects.all())
    course_name = forms.ModelChoiceField(queryset=CourseName.objects.all())
    mentorship = forms.BooleanField(required=False)
    description = forms.CharField(max_length=1000, required=False)

    def clean_password(self):
        MIN_LENGTH = 8
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("The new password must be at least 8 characters long.")
        return self.cleaned_data.get('password')

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data.get('email', None)).count() > 0:
            raise forms.ValidationError("User with this email already exists")

        req = ".ac.in"
        if req not in self.cleaned_data.get('email'):
            raise forms.ValidationError("sign up with your college account")

        return self.cleaned_data.get('email')

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data.get('username', None)).count() > 0:
            raise forms.ValidationError("User with this username already exists")

        return self.cleaned_data.get('username')

    def clean_gender(self):
        print("clean gender: ", self.cleaned_data)
        return self.cleaned_data.get('gender')

    def save(self, kwargs=None):
        print(self.cleaned_data)
        u = User.objects.create_user(first_name=self.cleaned_data.get('first_name'),
                                     last_name=self.cleaned_data.get('last_name'),
                                     email=self.cleaned_data.get('email'),
                                     password = self.cleaned_data.get('password'),
                                     username = self.cleaned_data.get('username'))
        u.save()
        s = FacultyRegistration.objects.create(user=u,
                                               gender=self.cleaned_data.get('gender'),
                                               college_name = self.cleaned_data.get('college_name'),
                                               course_name = self.cleaned_data.get('course_name'),
                                               mentorship=self.cleaned_data.get('mentorship'),
                                               description=self.cleaned_data.get('description'),
                                               )
        s.save()
        return u

class StudentEditProfile(UserChangeForm):

    class Meta:

        model=StudentRegistration
        fields=(
            'college_name',
            'password'
        )

class FacultyEditProfile(UserChangeForm):

    class Meta:

        model=FacultyRegistration
        fields=(
            'college_name',
            'mentorship',
            'description',
            'password'
        )


class AboutUsForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    gender = forms.ChoiceField(CHOICE, required=True)
    email = forms.EmailField(required=True,max_length=100)
    fb_id = forms.CharField(max_length=1000, required=True)
    linkedin = forms.CharField(max_length=1000, required=True)
    github = forms.CharField(max_length=1000, required=True)
    description = forms.CharField(max_length=10000, required=True)
    dp = forms.ImageField()

    def save(self, commit=False):
        a = AboutUs.objects.create(first_name=self.cleaned_data.get('first_name'),
                                   last_name=self.cleaned_data.get('last_name'),
                                   email=self.cleaned_data.get('email'),
                                   gender = self.cleaned_data.get('gender'),
                                   fb_id =self.cleaned_data.get('fb_id'),
                                   linkedin =self.cleaned_data.get('linkedin'),
                                   github =self.cleaned_data.get('github'),
                                   description = self.cleaned_data.get('description'),
                                   dp = self.cleaned_data.get('dp'),
                                   )
        a.save()
        return a

    def clean_gender(self):
        print("clean gender: ", self.cleaned_data)
        return self.cleaned_data.get('gender')

class CollegeNameForm(forms.Form):
    college_name = forms.CharField(max_length=200,required=True)
    college_images = forms.ImageField(required=False)

    def save(self, kwargs=None):
        print(self.cleaned_data)
        s = CollegeName.objects.create(college_name=self.cleaned_data.get('college_name'),
                                       college_images=self.cleaned_data.get('college_images'),
                                       )
        s.save()
        return s

class CourseNameForm(forms.Form):
    course_name = forms.CharField(max_length=200,required=True)

    def save(self, kwargs=None):
        print(self.cleaned_data)
        s = CourseName.objects.create(course_name=self.cleaned_data.get('course_name'),

                                      )
        s.save()
        return s
class TopicForm(forms.Form):
    title = forms.CharField(max_length=100,required=True)
    description = forms.CharField(max_length=1000,required=False)
    user_id = forms.CharField(max_length=1000, required=True, disabled=True,widget=forms.HiddenInput())

    def save(self, kwargs=None):
        t = Topic.objects.create(title=self.cleaned_data.get('title'),
                                 description=self.cleaned_data.get('description'),
                                 user_id=self.cleaned_data.get('user_id'))
        t.save()
        return t


class DocumentForm(forms.Form):
    document_name = forms.CharField(max_length=100,required=True)
    topic_id =forms.CharField(max_length=1000,required=True, disabled=True,widget=forms.HiddenInput())
    copyright = forms.ChoiceField(COPYRIGHT,required=True)
    document_file = forms.FileField(required=True)

    def clean_document_file(self):
        print("clean document_file: ", self.cleaned_data)
        return self.cleaned_data.get('document_file')

    def clean_documet_name(self):
        print("documet_name: ", self.cleaned_data)
        return self.cleaned_data.get('documet_name')


    def save(self, kwargs=None):
        d= Document.objects.create(document_name=self.cleaned_data.get('document_name'),
                                   topic_id = self.cleaned_data.get('topic_id'),
                                   copyright=self.cleaned_data.get('copyright'),
                                   document_file=self.cleaned_data.get('document_file'))

        d.save()
        return d

class VideoForm(forms.Form):
    video_name = forms.CharField(max_length=100, required=True)
    topic_id = forms.CharField(max_length=1000, required=True, disabled=True,widget=forms.HiddenInput())
    copyright = forms.ChoiceField(COPYRIGHT, required=True)
    video_file = forms.FileField(required=True)

    def clean_video_name(self):
        print("clean video_name: ", self.cleaned_data)
        return self.cleaned_data.get('video_name')

    def clean_video_file(self):
        print("clean video file: ", self.cleaned_data)
        return self.cleaned_data.get('video_file')

    def save(self, kwargs=None):
        v = Video.objects.create(video_name=self.cleaned_data.get('video_name'),
                                 topic_id=self.cleaned_data.get('topic_id'),
                                 copyright=self.cleaned_data.get('copyright'),
                                 video_file=self.cleaned_data.get('video_file'))

        v.save()
        return v


class CommentForm(forms.Form):
    content = forms.CharField(max_length=10000,required=True)
    time_stamp = forms.DateTimeField(required=True,disabled=True,widget=forms.HiddenInput())
    topic_id = forms.CharField(max_length=1000,required=True,disabled=True,widget=forms.HiddenInput())
    user_id = forms.CharField(max_length=1000,required=True,disabled=True,widget=forms.HiddenInput())

    def clean_content(self):
        print("clean content: ", self.cleaned_data)
        return self.cleaned_data.get('content')

    def save(self,kwargs=None):
        c=Comment.objects.create(content=self.cleaned_data.get('content'),
                                 time_stamp=self.cleaned_data.get('time_stamp'),
                                 topic_id=self.cleaned_data.get('topic_id'),
                                 user_id=self.cleaned_data.get('user_id'))
        c.save()
        return c


class DiscussionCommentForm(forms.ModelForm):
    class Meta:
        model = DiscussionComment
        fields = ['content', 'thread', 'user']

    def clean_content(self):
        return self.cleaned_data.get('content')

    def clean_thread(self):
        return self.cleaned_data.get('thread')

    def clean_user(self):
        return self.cleaned_data.get('user')


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['question', 'subject', 'user']
    def clean_question(self):
        return self.cleaned_data.get('question')
    def clean_subject(self):
        return self.cleaned_data.get('subject')
    def clean_user(self):
        return self.cleaned_data.get('user')

class QForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['question']

    def clean_question(self):
        return self.cleaned_data.get('question')