from django.shortcuts import render
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


def get_cat(request, cat_id):
    prs = Products.objects.filter(category_id=cat_id)
    cats = Category.objects.all()
    category = Category.objects.get(pk=cat_id)
    context = {
        'products': prs,
        'cats': cats,
        'category': category
    }
    return render(request, template_name='products/prod_of_cats.html', context=context)
