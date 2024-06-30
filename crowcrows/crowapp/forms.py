from django import forms
from .models import User
from ckeditor.widgets import CKEditorWidget


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'display_name', 'email', 'password')


class ResetPasswordForm(forms.ModelForm):
    old_password = forms.CharField(max_length=15, min_length=8, label='Old Password', )
    new_password = forms.CharField(max_length=15, min_length=8, label='New Password'),
    verify_password = forms.CharField(max_length=15, min_length=8, label='Repeat New Password'),


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')


