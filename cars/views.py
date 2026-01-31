from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
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


class NewCarCreateView(CreateView):
    model = Car
    form_class = CarModelForm
    template_name = 'new_car.html'
    success_url = reverse_lazy('cars_list')
    context_object_name = 'new_car_form'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_car_form'] = context.pop('form')
        return context


class CarUpdateView(LoginRequiredMixin, UpdateView):
    model = Car
    form_class = CarModelForm
    template_name = 'car_update.html'
    success_url = reverse_lazy('cars_list')
    login_url = 'login'


def car_detail_view(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'car_detail.html', {'car': car})
