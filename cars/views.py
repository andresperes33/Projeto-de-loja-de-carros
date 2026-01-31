from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from cars.models import Car
from .forms import CarModelForm


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
