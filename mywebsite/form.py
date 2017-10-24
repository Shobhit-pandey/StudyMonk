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
        pass

    def clean_gender(self):
        pass


class FacultyRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    gender = forms.ChoiceField(CHOICE)
    college_name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=1000)
    mentorship_status = forms.BooleanField()
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=100)


    def save(self):
        pass

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data.get('email', None)).count() > 0:
            raise forms.ValidationError("User with this email already exists")

        return self.cleaned_data.get('email')

    def clean_gender(self):
        pass
