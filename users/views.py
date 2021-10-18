from django.shortcuts import render


def login(request):
    return render(request, 'users/login.html', {'title': 'GeeShop - Авторизация'})


def register(request):
    return render(request, 'users/register.html', {'title': 'Geekshop - Регистрация'})
