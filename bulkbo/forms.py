from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import sender_number,sender_name

class register(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email','username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')

list_name = sender_name.objects.all()
for i in list_name:
    print(i.sendername)

    Select_country = (
        (i.sendername,i.sendername),
    )

Select_Service =(
    ("fb", 'Facebook'),
    ("go", 'Youtube/Gmail'),
    ("lf", 'TikTok'),
    ("ld", 'Lazada'),
    ("wb", 'WeChat'),
    ("ig", 'Instagram'),
    ('nz','FoodPanda'),
    ('ht','HotMail')
)


class Menu(forms.Form):
    select_country = forms.ChoiceField(label='SELECT COUNTRY',choices =Select_country,required=False)
    select_service = forms.ChoiceField(label='SELECT SERVICE',choices =Select_Service,required=False)

