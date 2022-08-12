import requests
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import register, LoginForm, sender_name_form, nunber_list_form,text_list_form
from .models import list_numbers, sender_name, UserAPI, report,text
from django.contrib.auth import get_user_model


@login_required(login_url='login')
def homepage(request):
    global i
    User = get_user_model()
    user = User.objects.get(id=request.user.id)
    # list sender name and number and text from model
    list_sender = sender_name.objects.filter(author=request.user.id)
    list_number = list_numbers.objects.filter(author=request.user.id)
    list_text = text.objects.filter(author=request.user.id)
    # get api id from from model user
    user_api = UserAPI.objects.filter(author=request.user.id).first()
    # balance request
    get_balance = requests.get(
        f'https://gateway.sms77.io/api/balance?p={user_api}')
    # check if user request as a post
    if request.method == 'POST':
        # get value from selection list number and sender name
        get_number = request.POST.getlist('getnumber')
        get_sender_name = request.POST.getlist('getsendername')
        get_text = request.POST.getlist('text')
        # convert list to integer
        a_string = "".join(get_number)
        # get list number with specific user and get the first value
        list_number = list_numbers.objects.filter(author=request.user.id, id=int(a_string))
        b_string = "".join(get_sender_name)
        list_sender_name = sender_name.objects.filter(author=request.user.id, id=int(b_string))
        c_string = "".join(get_text)
        list_Text = text.objects.filter(author=request.user.id, id=int(c_string))
        # start request data

        send_now = requests.get(
            f'http://gateway.sms77.io/api/sms?p={user_api}&to={str(list_number.first())}&text={str(list_Text.first())}&from={str(list_sender_name.first())}&debug=1&json=1')
        for all in send_now.json()['messages']:
            print(all)
            reports = report.objects.create(author=user, Recipient=all['recipient'], SenderID=all['sender'],
                                            Text=all['text'], Price=all['price'], TotalPrice=send_now.json()['total_price'])
            reports.save()

    return render(request, 'home.html',
                  {'balance': get_balance.text, 'numberlist': list_number, 'list_sender_name': list_sender,'listtext':list_text})


def registerview(request):
    global messages
    if request.method == 'POST':
        form = register(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = register()
    return render(request, 'register.html', {'form': form,'message':messages})


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'login.html'


@login_required(login_url='login')
def senderprofileview(request):
    if request.method == 'POST':
        sender_name = sender_name_form(request.POST)
        sender_number = nunber_list_form(request.POST)
        text = text_list_form(request.POST)
        if sender_name.is_valid():
            sender_name.save()
        if sender_number.is_valid():
            sender_number.save()
        if text.is_valid():
            text.save()
    else:
        sender_name = sender_name_form()
    user_api = UserAPI.objects.filter(author=request.user.id).first()
    # request display balance
    get_balance = requests.get(
        f'https://gateway.sms77.io/api/balance?p={user_api}')
    return render(request, 'config.html', {'form': sender_name,'balance':get_balance.text})

@login_required(login_url='login')
def reportviews(request):
    User = get_user_model()
    user = User.objects.get(id=request.user.id)
    list_reports = report.objects.filter(author=user)
    for i in list_reports:
        totalprice = i.TotalPrice
        print(totalprice)
    user_api = UserAPI.objects.filter(author=request.user.id).first()
    get_balance = requests.get(
        f'https://gateway.sms77.io/api/balance?p={user_api}')
    return render(request, 'reports.html',{'result':list_reports,'totalprice':totalprice,'balance':get_balance.text})


def getstartview(request):
    return render(request,'main.html')


