from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView


class OrderList(ListView):
    pass


class OrderCreate(CreateView):
    pass


class OrderUpdate(UpdateView):
    pass


class OrderDetail(DetailView):
    pass


class OrderDelete(DeleteView):
    pass


def order_forming_complete(request, pk):
    pass

