from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.db import connection
from products.models import Category, Products
from .forms import UserAdminRegisterForm, UserAdminEditForm, CategoryUpdateFormAdmin
from .utils import SuperUserMixin

from users.models import User


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


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


class CategoryListView(ListView):
    model = Category
    template_name = 'myadmin/admin-category-read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'Myadmin :: Категории'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryListView, self).dispatch(request, *args, **kwargs)


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'myadmin/admin-category-update-delete.html'
    success_url = reverse_lazy('myadmin:admin_category')

    def post(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.product_set.update(is_active=False)
        self.object.is_active = False
        self.object.save()

        category = Category.objects.all()
        context = {'object_list': category}
        result = render_to_string('myadmin/delete_category.html', context, request=request)
        return JsonResponse({'result': result})

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryDeleteView, self).dispatch(request, *args, **kwargs)


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'myadmin/admin-category-update-delete.html'
    success_url = reverse_lazy('myadmin:admin_category')
    form_class = CategoryUpdateFormAdmin

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                print(f'применяется скидка {discount} % к товарам категории {self.object.title}')
                self.object.products_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        obj = self.get_object()
        context['key'] = obj.id
        context['cat'] = obj.title
        return context


# Product

class ProductListView(ListView):
    model = Products
    template_name = 'myadmin/admin-product-read.html'

    def get_queryset(self):
        return Products.objects.all().select_related()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Администрирование :: Продукты'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductListView, self).dispatch(request, *args, **kwargs)
