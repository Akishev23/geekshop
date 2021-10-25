from django.urls import path
from .views import ProductPage

app_name = 'products'

urlpatterns = [
    path('', ProductPage.as_view(), name='products'),
]
