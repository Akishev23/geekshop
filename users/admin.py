from django.contrib import admin

from baskets.admin import BasketAdmin
from .models import User
from baskets.models import Basket


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = Basket
    inlines = (BasketAdmin,)
