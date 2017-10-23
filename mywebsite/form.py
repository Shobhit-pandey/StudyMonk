from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class StudentRegistration(UserCreationForm):
    #choice= ('Male' , 'Female','Other')
    username = forms.CharField(max_length=100)
    StudentId = forms.IntegerField(max_value=10000000000000)
    FirstName = forms.CharField(max_length=100)
    LastName = forms.CharField(max_length=100)
    EmailId = forms.EmailField()
    CollegeName = forms.CharField(max_length=1000)
    Gender = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'FirstName', 'LastName', 'EmailId','CollegeName','Gender', 'password1', 'password2',)


    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data.get('email', None)).count() > 0:
            raise forms.ValidationError("User with this email already exists")

        return self.cleaned_data.get('email')


    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data.get('username', None)).count() > 0:
            raise forms.ValidationError("User with this username already exists")

        return self.cleaned_data.get('username')


class FacultyRegistration(UserCreationForm):
    #choice= ('Male' , 'Female','Other')
    username = forms.CharField(max_length=100)
    FacultyId = forms.IntegerField(max_value=10000000000000)
    FirstName = forms.CharField(max_length=100)
    LastName = forms.CharField(max_length=100)
    EmailId = forms.EmailField()
    CollegeName = forms.CharField(max_length=1000)
    Gender = forms.CharField(max_length=100)
    Description = forms.CharField(max_length=10000)
    Mentorship = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ('username', 'FirstName', 'LastName', 'EmailId','CollegeName','Gender', 'password1', 'password2',)


    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data.get('email', None)).count() > 0:
            raise forms.ValidationError("User with this email already exists")

        return self.cleaned_data.get('email')


    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data.get('username', None)).count() > 0:
            raise forms.ValidationError("User with this username already exists")

        return self.cleaned_data.get('username')