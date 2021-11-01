from django.conf import settings
from django.db import models

# Create your models here.

from products.models import Products


class Order(models.Model):
    FORMING = 'FM'
    SEND_TO_PROCEED = 'STP'
    PAID = 'PD'
    PROCEEDED = 'PRD'
    READY = 'RD'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SEND_TO_PROCEED, 'отправлен в работу'),
        (PAID, 'Оплачен'),
        (PROCEEDED, 'В работе'),
        (READY, 'Готов к выдаче'),
        (CANCEL, 'Отменен')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, verbose_name='Статус заказа',
                              max_length=3, default='FM')

    def __str__(self):
        return f'Текущий заказ {self.pk}'

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.get_product_cost(), items)))

    def get_items(self):
        pass


class OrderItems(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='orderitems',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name='Продукты', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity
