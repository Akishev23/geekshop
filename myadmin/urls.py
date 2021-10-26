from django.urls import path
from .views import index, UserListView, UserUpdateView, UserCreateView, UserDeleteView
from products.admin import ProductsAdmin

app_name = 'myadmin'

urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='users'),
    path('user_update/<int:pk>', UserUpdateView.as_view(), name='user_update'),
    path('user_create/', UserCreateView.as_view(), name='user_create'),
    path('user_delete/<int:pk>', UserDeleteView.as_view(), name='user_delete')
]
