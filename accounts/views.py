from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
import urllib.request
import urllib.parse
import json


def register_view(request):
   if request.method == 'POST':
        user_form = UserCreationForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            
            # Notificação Telegram
            if settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID:
                try:
                    text = f"👤 *Novo Usuário Cadastrado!*\n\n*Username:* {user.username}\n*E-mail:* {user.email if user.email else 'Não informado'}"
                    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
                    data = urllib.parse.urlencode({'chat_id': settings.TELEGRAM_CHAT_ID, 'text': text, 'parse_mode': 'Markdown'}).encode()
                    req = urllib.request.Request(url, data=data)
                    urllib.request.urlopen(req)
                except Exception:
                    pass

            # Notificação WhatsApp (Z-API)
            if settings.WHATSAPP_INSTANCE_ID and settings.WHATSAPP_TOKEN:
                try:
                    text = f"👤 *Novo Usuário Cadastrado!*\n\n*Username:* {user.username}\n*E-mail:* {user.email if user.email else 'Não informado'}"
                    url = f"https://api.z-api.io/instances/{settings.WHATSAPP_INSTANCE_ID}/token/{settings.WHATSAPP_TOKEN}/send-text"
                    
                    data = json.dumps({
                        'phone': settings.WHATSAPP_NUMBER,
                        'message': text
                    }).encode('utf-8')
                    
                    req = urllib.request.Request(url, data=data, method='POST')
                    req.add_header('Content-Type', 'application/json')
                    urllib.request.urlopen(req)
                except Exception:
                    pass
            
            return redirect('login')
   else:
        user_form = UserCreationForm()
    
    # Renderiza o template com o formulário
   return render(request, 'register.html', {'user_form': user_form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('cars_list')

    login_form = AuthenticationForm()
    return render(request, 'login.html', {'login_form': login_form})


def logout_view(request):
    logout(request)
    return redirect('cars_list')





