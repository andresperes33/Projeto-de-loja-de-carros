from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from cars.models import Car
from .forms import CarModelForm, MessageForm
from django.core.mail import send_mail
from django.conf import settings
import urllib.request
import urllib.parse


class CarsListView(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('model')
        search = self.request.GET.get('search')
        
        if search:
            queryset = queryset.filter(model__icontains=search)
        
        return queryset


class NewCarCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Car
    form_class = CarModelForm
    template_name = 'new_car.html'
    context_object_name = 'new_car_form'
    login_url = 'login'
    success_message = 'Carro cadastrado com sucesso!'
    
    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_car_form'] = context.pop('form')
        return context


class CarUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Car
    form_class = CarModelForm
    template_name = 'car_update.html'
    login_url = 'login'
    success_message = 'Carro atualizado com sucesso!'

    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs={'pk': self.object.pk})


class CarDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = reverse_lazy('cars_list')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, "Carro excluído com sucesso!")
        return super().form_valid(form)


def car_detail_view(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'car_detail.html', {'car': car})

def about_view(request):
    return render(request, 'about.html')


def contact_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # Salva no Banco de Dados
            message_obj = form.save()
            
            # Prepara o e-mail e Telegram
            subject = f"Novo contato: {message_obj.subject}"
            email_body = f"Nome: {message_obj.name}\nE-mail: {message_obj.email}\nAssunto: {message_obj.subject}\n\nMensagem:\n{message_obj.message}"
            
            # Envia para o Telegram if configurado
            if settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID:
                try:
                    text = f"🚗 *Novo Contato no Site!*\n\n*Nome:* {message_obj.name}\n*E-mail:* {message_obj.email}\n*Assunto:* {message_obj.subject}\n\n*Mensagem:* {message_obj.message}"
                    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
                    data = urllib.parse.urlencode({'chat_id': settings.TELEGRAM_CHAT_ID, 'text': text, 'parse_mode': 'Markdown'}).encode()
                    req = urllib.request.Request(url, data=data)
                    urllib.request.urlopen(req)
                except Exception:
                    pass

            try:
                send_mail(
                    subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL, # Remetente configurado
                    [settings.NOTIFY_EMAIL], # Destinatário (seu e-mail)
                    fail_silently=False,
                )
                messages.success(request, 'Sua mensagem foi enviada com sucesso! Entraremos em contato em breve.')
            except Exception:
                # Mesmo se o e-mail falhar, já salvamos no banco de dados.
                messages.success(request, 'Sua mensagem foi recebida e salva em nosso sistema. Obrigado!')
            
            return redirect('contact')
    else:
        form = MessageForm()
    
    return render(request, 'contact.html', {'form': form})
