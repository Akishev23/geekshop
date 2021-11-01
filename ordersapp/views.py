from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from ordersapp.models import Order


class OrderList(ListView):
    model = Order

    def ger_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)


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

