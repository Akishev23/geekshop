from django.urls import path
from .views import index, products, get_cat

app_name = 'products'

urlpatterns = [
    path('index/', index, name='index'),
    path('', products, name='products'),
]
