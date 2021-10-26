from django.contrib import admin

# Register your models here.

from baskets.models import Basket


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    extra = 0

