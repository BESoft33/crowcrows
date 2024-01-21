from django import forms


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    user_email = forms.EmailField(max_length=100, label='Email')
    user_password = forms.CharField(
        max_length=15,
        min_length=8,
        label='Password',
        help_text='Password must be of length 8 characters to 15 characters')
    verify_password = forms.CharField(max_length=15, min_length=8, label='Repeat Password')


class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(max_length=15, min_length=8, label='Old Password', )
    new_password = forms.CharField(max_length=15, min_length=8, label='New Password'),
    verify_password = forms.CharField(max_length=15, min_length=8, label='Repeat New Password'),


class LoginForm(forms.Form):
    user_email = forms.EmailField(max_length=100)
    user_password = forms.CharField(max_length=15, min_length=8,
                                    help_text='Password must be of length 8 characters to 15 characters')
