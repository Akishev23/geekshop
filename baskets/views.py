from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.template.loader import render_to_string
from products.models import Products
from baskets.models import Basket


# Create your views here.
@login_required
def basket_add(request, product_id):
    product = Products.objects.get(pk=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, product_id):
    Basket.objects.get(id=product_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, good_id, good_quantity):
    if request.is_ajax():
        basket = Basket.objects.get(pk=good_id)
        if good_quantity > 0:
            basket.quantity = good_quantity
            basket.save()
        else:
            basket.delete()

    baskets = Basket.objects.filter(user=request.user)
    result = render_to_string('inc_baskets/_baskets.html', {'baskets': baskets})
    return JsonResponse({'result': result})
