from django.conf import settings
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from django.views.generic import CreateView, UpdateView
from baskets.models import Basket
from myadmin.utils import SuperUserMixin
from users.forms import UserRegisterForm, UserProfileForm
from django.urls import reverse_lazy, reverse
from .forms import UserLoginForm
from products.utils import *
from django.contrib import messages
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
        if form.is_valid():
            user = form.save()
            mes = messages.success(self.request, 'Вы успешно зарегистрировались')
            user.save()

            verify_link = reverse('users:verify', args=[user.email, user.activation_key])
            subject = f'Активация учетной записи'
            message = f'Для подтверждения учетной записи {user.username} перейдите по ссылке \n' \
                      f'{settings.DOMAIN_NAME}{verify_link}'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email],
                      fail_silently=False)

            return redirect('users:login')
        else:
            raise ValueError('something wrong with form')


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


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user and user.activation_key == activation_key and not user.is_activation_key_expired():
            user.activation_key = ''
            user.activation_key_created = None
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'users/verification.html')
    except Exception as e:
        return HttpResponseRedirect(reverse('users:login'))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)
