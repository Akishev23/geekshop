from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView
from baskets.models import Basket
from users.forms import UserRegisterForm, UserProfileForm
from django.urls import reverse_lazy
from .forms import UserLoginForm
from products.utils import *
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User


class UserLogin(BaseContextMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    title = 'Geekshop :: Авторизация'

    def get_success_url(self):
        return reverse_lazy('products:products')


class RegisterUser(BaseContextMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('index')
    title = 'Geekshop :: Регистрация'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('products:products')


class UserProfile(LoginRequiredMixin, BaseContextMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_message = "Profile Updated"
    success_url = "."
    title = 'GeekShop :: Обновление профиля'

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return user

    def get_queryset(self):
        base_qs = super(UserProfile, self).get_queryset()
        return base_qs.filter(username=self.request.user.pk)


def logout_user(request):
    logout(request)
    return redirect('users:login')
