from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model

MyUser = get_user_model()


class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        label = 'Username',
        max_length = 100,
        min_length = 5,
        widget = forms.TextInput(attrs = {
            'class': 'form-control'
        }))

    email = forms.EmailField(
        label = 'Email',
        max_length = 35,
        min_length = 5,
        widget = forms.EmailInput(attrs = {
            'class': 'form-control'
        }))

    password1 = forms.CharField(
        label = 'Password',
        max_length = 50,
        min_length = 5,
        widget = forms.PasswordInput(attrs = {
            'class': 'form-control'
        }))

    password2 = forms.CharField(
        label = 'Confirm Password',
        max_length = 50, min_length = 5,
        widget = forms.PasswordInput(attrs = {
            'class': 'form-control'
        }))


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    email = forms.EmailField(
        label = "",
        required = True,
        widget = forms.EmailInput(attrs = {
            "placeholder":"Valid Email",
            "type":"email",
            "name":"email",
            "class":"form-control ",
        }))

    class Meta:
        model = MyUser
        fields = ("email")


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    new_password1 = forms.CharField(
        label = "",
        required = True,
        help_text = "",
        widget = forms.PasswordInput(attrs = {
            "placeholder":"password",
            "type":"password",
            "name":"password1",
            "class":"form-control mt-2",
        }))

    new_password2 = forms.CharField(
        label = "",
        required = True,
        help_text = "",
        widget = forms.PasswordInput(attrs = {
            "placeholder":"confirm password",
            "type":"password",
            "name":"password1",
            "class":"form-control mt-2",
        }))

    class Meta:
        model = MyUser
        fields = ("new_password1","new_password2")
