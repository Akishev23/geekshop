from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.contrib import messages

from baskets.models import Basket
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from django.contrib import auth
from django.urls import reverse


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                auth.login(request, user)
                messages.success(request, 'Вы успешно вошли на сайт')
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


@login_required
def profile(request):
    user_req = request.user
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=user_req, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные сохранены успешно')
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            messages.error(request, 'Ошибка сохранения')
    baskets = Basket.objects.filter(user=user_req)
    context = {
        'title': 'Личный кабинет',
        'form': UserProfileForm(instance=user_req),
        'baskets': baskets
    }

    return render(request, 'users/profile.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('products:index'))
