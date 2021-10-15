from django.shortcuts import render
import json
from .models import Category, Products


# Create your views here.

def index(request):
    context = {
        'title': 'index',
    }
    return render(request, 'products/index.html', context)


def products(request):
    cats = Category.objects.all()
    prs = Products.objects.all()
    context = {
        'title': 'products',
        'products': prs,
        'cats': cats
    }
    return render(request, 'products/products.html', context)
