from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from baskets.models import Basket
from users.forms import UserRegisterForm, UserProfileForm
from django.urls import reverse, reverse_lazy
from .forms import UserLoginForm
from products.utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from extra_views import InlineFormSetView

from .models import User


class UserLogin(ContextMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='GeeShop :: Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('products:products')


class RegisterUser(ContextMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='GeeShop :: Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('products:products')


class UserProfile(LoginRequiredMixin, ContextMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_message = "Profile Updated"
    success_url = "."

    def get_context_data(self, *args, **kwargs):
        user_req = self.request.user
        context = super(UserProfile, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='GeeShop :: Профиль пользователя')
        c_form = self.get_user_context(form=UserProfileForm(instance=user_req))
        c_bas = self.get_user_context(baskets=Basket.objects.filter(user=user_req))
        return dict(list(context.items()) + list(c_def.items()) + list(c_form.items()) +
                    list(c_bas.items()))

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return user

    def get_queryset(self):
        base_qs = super(UserProfile, self).get_queryset()
        return base_qs.filter(username=self.request.user.pk)


def logout_user(request):
    logout(request)
    return redirect('users:login')
