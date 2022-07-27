from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm

class register(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')
