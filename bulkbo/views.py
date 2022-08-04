import requests
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import register, LoginForm,sender_name_form,nunber_list_form
from .models import list_numbers,sender_name,UserAPI,report
from django.contrib.auth import get_user_model

@login_required(login_url='login')
def homepage(request):
    global i
    User = get_user_model()
    user = User.objects.get(id=request.user.id)
    # list sender name and number from model
    list_sender = sender_name.objects.filter(author=request.user.id)
    list_number = list_numbers.objects.filter(author=request.user.id)
    #get api id from from model user
    user_api = UserAPI.objects.filter(author=request.user.id).first()
    #balance request
    get_balance = requests.get(
        f'https://gateway.sms77.io/api/balance?p={user_api}')
    # check if user request as a post
    if request.method =='POST':
        # get value from selection list number and sender name
        get_number = request.POST.getlist('getnumber')
        get_sender_name = request.POST.getlist('getsendername')
        #convert list to integer
        a_string = "".join(get_number)
        #get list number with specific user and get the first value
        list_number = list_numbers.objects.filter(author=request.user.id, id=int(a_string))
        b_string = "".join(get_sender_name)
        list_sender_name = sender_name.objects.filter(author=request.user.id, id=int(b_string))
        # start request data

        send_now = requests.get(
            f'http://gateway.sms77.io/api/sms?p={user_api}&to={str(list_number.first())}&text=Test+SMS&from={str(list_sender_name.first())}&debug=1&json=1')
        result = [send_now.json()['total_price'],send_now.json()['messages'][0]['sender']]
        for all in send_now.json()['messages']:
            reports = report.objects.create(author=user, Recipient=all['recipient'], SenderID=all['sender'],
                                            Text=all['text'], Price=2.2, TotalPrice=2.2)
            reports.save()
        print(result)
    return render(request, 'home.html', {'balance': get_balance.text,'numberlist':list_number,'list_sender_name':list_sender})


def registerview(request):
    if request.method == 'POST':
        form = register(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            messages.success(request, 'Register successfully!')
            return redirect('/login')
    else:
        form = register()
    return render(request, 'register.html', {'form': form})


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'login.html'

@login_required(login_url='login')
def senderprofileview(request):
    if request.method == 'POST':
        sender_name = sender_name_form(request.POST)
        sender_number = nunber_list_form(request.POST)
        if sender_name.is_valid():
            sender_name.save()
        if sender_number.is_valid():
            sender_number.save()
    else:
        sender_name = sender_name_form()
    return render(request,'config.html',{'form':sender_name})

def reportviews(request):
    return render(request,'reports.html')