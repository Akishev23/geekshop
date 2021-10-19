from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.contrib import messages
from users.forms import UserLoginForm, UserRegisterForm
from django.contrib import auth
from django.urls import reverse


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('products:index'))
        else:
            messages.error(request, 'Ошибка входа!')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'title': 'GeeShop - Авторизация',
                                                'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            messages.success(request, 'Вы успешно зарегистрированы')
            return HttpResponseRedirect(reverse('products:index'))
        else:
            messages.error(request, 'Ошибка регистрации!')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'title': 'Geekshop - Регистрация',
                                                   'form': form})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('products:index'))
