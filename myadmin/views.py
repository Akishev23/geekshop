from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from .forms import UserAdminRegisterForm, UserAdminEditForm
from .utils import SuperUserMixin

# Create your views here.
from users.models import User


@login_required
def index(request):
    return render(request, 'myadmin/admin.html')


class UserListView(SuperUserMixin, ListView):
    model = User
    template_name = 'myadmin/admin-users-read.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'Geekshop :: Панель администратора'
        return context


class UserCreateView(SuperUserMixin, CreateView):
    model = User
    template_name = 'myadmin/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('myadmin:users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Geekshop :: Создание пользователя'
        return context


class UserUpdateView(SuperUserMixin, UpdateView):
    model = User
    template_name = 'myadmin/admin-users-update-delete.html'
    form_class = UserAdminEditForm
    success_url = reverse_lazy('myadmin:users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Geekshop :: Обновление пользователя'
        return context


class UserDeleteView(SuperUserMixin, DeleteView):
    model = User
    template_name = 'myadmin/admin-users-update-delete.html'
    success_url = reverse_lazy('myadmin:users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())
