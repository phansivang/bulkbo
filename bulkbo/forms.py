from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import list_numbers,sender_name,text


class register(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email','username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')

class sender_name_form(forms.ModelForm):
    class Meta:
        model = sender_name
        fields = ['sendername','author']

class nunber_list_form(forms.ModelForm):
    class Meta:
        model = list_numbers
        fields = '__all__'

class text_list_form(forms.ModelForm):
    class Meta:
        model = text
        fields = '__all__'