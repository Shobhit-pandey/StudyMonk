from django import forms
from django.contrib.auth.models import User

from mywebsite.models import StudentRegistration, FacultyRegistration

CHOICE = (
    ('male', 'male'),
    ('female', 'female'),
    ('other','other')
)

class StudentRegistrationForm(forms.Form):

    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    gender = forms.ChoiceField(CHOICE)
    college_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=100)

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data.get('email', None)).count() > 0:
            raise forms.ValidationError("User with this email already exists")

        return self.cleaned_data.get('email')

    def save(self):
        print(self.cleaned_data)
        u = User.objects.create_user(first_name=self.cleaned_data.get('first_name'),last_name=self.cleaned_data.get('last_name'),email=self.cleaned_data.get('email')
                                ,password = self.cleaned_data.get('password'),username = self.cleaned_data.get('username'))
        u.save()
        s = StudentRegistration.objects.create(user=u, gender=self.cleaned_data.get('gender'),
                                               college_name = self.cleaned_data.get('college_name'))
        s.save()

    def clean_gender(self):
        print("clean gender: ", self.cleaned_data)
        return self.cleaned_data.get('gender')


class FacultyRegistrationForm(forms.Form):

    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    gender = forms.ChoiceField(CHOICE)
    college_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=100)
    description = forms.CharField(max_length=1000,required=False)
    mentorship_status = forms.BooleanField(required=False)

    def save(self):
        print(self.cleaned_data)
        u = User.objects.create(first_name=self.cleaned_data.get('first_name'),
                                last_name=self.cleaned_data.get('last_name'),
                                email=self.cleaned_data.get('email'),
                                password=self.cleaned_data.get('password'),
                                username=self.cleaned_data.get('username'))
        u.save()
        s = FacultyRegistration.objects.create(user=u, gender=self.cleaned_data.get('gender'),
                                               college_name=self.cleaned_data.get('college_name'),
                                               description = self.cleaned_data.get('description'),
                                               mentorship_status = self.cleaned_data.get('mentorship_status'),
                                               )
        s.save()

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data.get('email', None)).count() > 0:
            raise forms.ValidationError("User with this email already exists")

        return self.cleaned_data.get('email')

    def clean_gender(self):
        print("clean gender: ", self.cleaned_data)
        return self.cleaned_data.get('gender')
