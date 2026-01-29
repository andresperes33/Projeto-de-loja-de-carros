from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
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
