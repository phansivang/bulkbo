import requests
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, SenderNameForm, NumberListForm, TextListForm
from .models import ListNumbers, SenderName, UserAPI, Report, Text
from django.contrib.auth import get_user_model
from django.http import HttpResponse

@login_required(login_url='login')
def homepage(request):
    user = request.user
    list_senders = SenderName.objects.filter(author=user)
    list_numbers = ListNumbers.objects.filter(author=user)
    list_texts = Text.objects.filter(author=user)
    user_api = UserAPI.objects.filter(author=user).first()

    if user_api:
        balance_response = requests.get(f'https://gateway.sms77.io/api/balance?p={user_api.api_key}')
        balance = balance_response.text if balance_response.status_code == 200 else "Error fetching balance"
    else:
        balance = "No API key found"

    if request.method == 'POST':
        selected_number_id = request.POST.get('getnumber')
        selected_sender_id = request.POST.get('getsendername')
        selected_text_id = request.POST.get('text')

        try:
            selected_number = ListNumbers.objects.get(author=user, id=selected_number_id)
            selected_sender = SenderName.objects.get(author=user, id=selected_sender_id)
            selected_text = Text.objects.get(author=user, id=selected_text_id)
        except (ListNumbers.DoesNotExist, SenderName.DoesNotExist, Text.DoesNotExist):
            messages.error(request, "Invalid selection")
            return redirect('homepage')

        send_now_response = requests.get(
            f'http://gateway.sms77.io/api/sms?p={user_api.api_key}&to={selected_number.number}&text={selected_text.text}&from={selected_sender.name}&json=1'
        )

        if send_now_response.status_code == 200:
            response_json = send_now_response.json()
            for message in response_json.get('messages', []):
                Report.objects.create(
                    author=user,
                    Recipient=message['recipient'],
                    SenderID=message['sender'],
                    Text=message['text'],
                    Price=message['price'],
                    TotalPrice=response_json['total_price']
                )
            messages.success(request, "Messages sent successfully")
        else:
            messages.error(request, "Error sending messages")

    return render(request, 'home.html', {
        'balance': balance,
        'numberlist': list_numbers,
        'list_sender_name': list_senders,
        'list_text': list_texts
    })

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'login.html'

@login_required(login_url='login')
def sender_profile_view(request):
    if request.method == 'POST':
        sender_name_form = SenderNameForm(request.POST)
        sender_number_form = NumberListForm(request.POST)
        text_form = TextListForm(request.POST)
        if sender_name_form.is_valid():
            sender_name_form.save()
        if sender_number_form.is_valid():
            sender_number_form.save()
        if text_form.is_valid():
            text_form.save()
    else:
        sender_name_form = SenderNameForm()

    user_api = UserAPI.objects.filter(author=request.user).first()
    if user_api:
        balance_response = requests.get(f'https://gateway.sms77.io/api/balance?p={user_api.api_key}')
        balance = balance_response.text if balance_response.status_code == 200 else "Error fetching balance"
    else:
        balance = "No API key found"

    return render(request, 'config.html', {
        'form': sender_name_form,
        'balance': balance
    })

@login_required(login_url='login')
def report_view(request):
    user = request.user
    list_reports = Report.objects.filter(author=user)
    total_price = sum(report.TotalPrice for report in list_reports)

    user_api = UserAPI.objects.filter(author=user).first()
    if user_api:
        balance_response = requests.get(f'https://gateway.sms77.io/api/balance?p={user_api.api_key}')
        balance = balance_response.text if balance_response.status_code == 200 else "Error fetching balance"
    else:
        balance = "No API key found"

    return render(request, 'reports.html', {
        'result': list_reports,
        'totalprice': total_price,
        'balance': balance
    })

def get_start_view(request):
    return render(request, 'main.html')
