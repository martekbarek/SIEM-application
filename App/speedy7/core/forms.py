from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email','is_active','first_name','last_name' ]
        