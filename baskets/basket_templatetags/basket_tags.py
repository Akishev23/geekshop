from django import template

from baskets.models import Basket

register = template.Library()


@register.simple_tag()
def get_baskets(user):
    return Basket.objects.filter(user=user)
