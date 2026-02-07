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

            # Notificação WhatsApp (Evolution API)
            if settings.WHATSAPP_BASE_URL and settings.WHATSAPP_INSTANCE and settings.WHATSAPP_TOKEN:
                try:
                    text = f"👤 *Novo Usuário Cadastrado!*\n\n*Username:* {user.username}\n*E-mail:* {user.email if user.email else 'Não informado'}"
                    
                    base_url = settings.WHATSAPP_BASE_URL.rstrip('/')
                    instance_encoded = urllib.parse.quote(settings.WHATSAPP_INSTANCE)
                    url = f"{base_url}/message/sendText/{instance_encoded}"
                    
                    number = settings.WHATSAPP_NUMBER
                    number = ''.join(filter(str.isdigit, number))

                    data = json.dumps({
                        'number': number,
                        'text': text
                    }).encode('utf-8')
                    
                    req = urllib.request.Request(url, data=data, method='POST')
                    req.add_header('Content-Type', 'application/json')
                    req.add_header('apikey', settings.WHATSAPP_TOKEN)
                    
                    with urllib.request.urlopen(req) as response:
                        print(f"EVOLUTION_API: Cadastro enviado! Status: {response.getcode()}")
                except Exception as e:
                    print(f"EVOLUTION_API_ERROR: {str(e)}")
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





