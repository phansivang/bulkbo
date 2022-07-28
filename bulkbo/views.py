import requests
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import senderprofile
from .forms import register, LoginForm


@login_required(login_url='login')
def homepage(request):
    get_balance = requests.get(
        'https://gateway.sms77.io/api/balance?p=')
    return render(request, 'home.html', {'balance': get_balance.text})


def registerview(request):
    if request.method == 'POST':
        form = register(request.POST)
        if form.is_valid():
            print(1)
            form.save()
            messages.success(request, 'Register successfully!')
            return redirect('/login')
    else:
        form = register()
        print(2)
    print(3)
    return render(request, 'register.html', {'form': form})


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'login.html'


def configview(request):
    return render(request, 'config.html')

def testing(request):
    x = senderprofile.objects.all()
    for i in x:
        print(i.sender_name)
        print(len(i.number_list))
    return render(request,'home.html',{'home':x})