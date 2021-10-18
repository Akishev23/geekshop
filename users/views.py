from django.http import HttpResponseRedirect
from django.shortcuts import render

from users.forms import UserLoginForm, UserRegisterForm
from django.contrib import auth
from django.urls import reverse


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
        else:
            print(form.errors)
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'title': 'GeeShop - Авторизация',
                                                'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:login'))
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'title': 'Geekshop - Регистрация',
                                                   'form': form})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
