from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from mywebsite.models import StudentRegistration, FacultyRegistration, AboutUs, CollegeName, CourseName, Topic

CHOICE = (
    ('male', 'male'),
    ('female', 'female'),
    ('other','other')
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
        if User.objects.filter(password=self.cleaned_data.get('password', None)).size() < 8:
            raise forms.ValidationError("password should be atleast 8 digit")

        return self.cleaned_data.get('password')

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data.get('email', None)).count() > 0:
            raise forms.ValidationError("User with this email already exists")

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
        if User.objects.filter(password=self.cleaned_data.get('password', None)).__sizeof__() < 8:
            raise forms.ValidationError("password should be atleast 8 digit")

        return self.cleaned_data.get('password')

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data.get('email', None)).count() > 0:
            raise forms.ValidationError("User with this email already exists")

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

    def save(self, kwargs=None):
        t = Topic.objects.create(title=self.cleaned_data.get('title'),
                                 description=self.cleaned_data.get('description'))
        t.save()
        return t