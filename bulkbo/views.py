import requests
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import register,LoginForm
from django.contrib.auth import views as auth_views
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required(login_url='login')
def homepage(request):
    get_balance = requests.get(
        'https://gateway.sms77.io/api/balance?p=w8f7Cjk6jKEH7NkyAiuNZ4PQn25wXbjGINLqKW7adpeaQpunakzV276X3Zn3jgS9')
    return render(request,'home.html',{'balance':get_balance.text})

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
    return render(request,'config.html')