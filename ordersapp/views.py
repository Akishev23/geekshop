from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from baskets.models import Basket
from ordersapp.models import Order, OrderItems
from products.utils import BaseContextMixin
from .forms import OrderItemsForm


class OrderList(ListView):
    model = Order

    def ger_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)


class OrderCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:orders')

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        context['title'] = 'Geekshop :: Создать заказ'

        OrderFormSet = inlineformset_factory(Order, OrderItems, form=OrderItemsForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)

        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items:
                OrderFormSet = inlineformset_factory(Order, OrderItems, form=OrderItemsForm,
                                                     extra=basket_items.count())
                formset = OrderFormSet()

                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].price
                basket_items.delete()
            else:
                formset = OrderFormSet()

        context['orderitems'] = formset

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            if not self.object.get_total_cost():
                self.object.delete()

        return super(OrderCreate, self).form_valid(form)


class OrderUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:orders')

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        context['title'] = 'Geekshop :: Изменить заказ'

        OrderFormSet = inlineformset_factory(Order, OrderItems, form=OrderItemsForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)

        else:
                formset = OrderFormSet(instance=self.object)

                for form in formset:
                    if form.instance.pk:
                        form.initial['price'] = form.instance.product.price

        context['orderitems'] = formset

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            if not self.object.get_total_cost():
                self.object.delete()

        return super(OrderUpdate, self).form_valid(form)


class OrderDetail(DetailView):
    model = Order
    title = 'GeekShop :: Просмотр заказа'


class OrderDelete(BaseContextMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('orders:orders')


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SEND_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse_lazy('orders:orders'))