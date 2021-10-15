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
    cats = [cat for cat in Category.objects.all()]
    prs = [pr for pr in Products.objects.all()]
    context = {
        'title': 'products',
        'products': prs,
        'cats': cats
    }
    return render(request, 'products/products.html', context)
