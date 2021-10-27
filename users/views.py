from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView
from baskets.models import Basket
from myadmin.utils import SuperUserMixin
from users.forms import UserRegisterForm, UserProfileForm
from django.urls import reverse_lazy
from .forms import UserLoginForm
from products.utils import *

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


class UserProfile(SuperUserMixin, BaseContextMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_message = "Profile Updated"
    success_url = "."
    title = 'GeekShop :: Обновление профиля'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, pk=self.kwargs['pk'])

    def get_queryset(self):
        base_qs = super(UserProfile, self).get_queryset()
        return base_qs.filter(username=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES, instance=self.get_object())
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return redirect(self.success_url)


def logout_user(request):
    logout(request)
    return redirect('users:login')
