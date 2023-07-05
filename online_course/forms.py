from django import forms
from accounts.models import Account
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    role_choice = (
        ('teacher', 'Teacher'),
        ('student', 'Student')
    )
    role = forms.ChoiceField(required=True, help_text='Required. Add a valid role teacher or student',choices=role_choice)
    # role = forms.CharField(required=True, max_length=7, help_text='Required. Add a valid role teacher or student')
    class Meta:
        model = Account
        fields = ['email','username','role','password1','password2']
        # fields = '__all__'