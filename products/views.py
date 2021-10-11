from django.shortcuts import render
import json


# Create your views here.

def index(request):
    context = {
        'title': 'index',
    }
    return render(request, 'products/index.html', context)


def products(request):
    with open('products/fixtures/prod.json', encoding='utf-8') as f:
        prs = json.load(f)
    context = {
        'title': 'products',
        'products': prs
    }
    return render(request, 'products/products.html', context)
