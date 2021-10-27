from django.shortcuts import render
from .models import Category, Products
from django.views.generic import ListView
from .utils import *


class ProductPage(ContextMixin, ListView):
    model = Products
    template_name = 'products/products.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='GeekShop - список товаров')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Products.objects.filter(is_published=True)


def index(request):
    context = {
        'title': 'Geekshop - Главная страница',
    }
    return render(request, 'products/index.html', context)


class GetCategory(ContextMixin, ListView):
    model = Products
    template_name = 'products/prod_of_cats.html'
    context_object_name = 'products'
    allow_empty = False
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = Category.objects.get(pk=self.kwargs["cat_id"])
        c_def = self.get_user_context(title=f'GeekShop - '
                                            f'{cat}')
        c_cat = self.get_user_context(category=cat)
        return dict(list(context.items()) + list(c_def.items()) + list(c_cat.items()))

    def get_queryset(self):
        return Products.objects.filter(category_id=self.kwargs['cat_id'], is_published=True)
