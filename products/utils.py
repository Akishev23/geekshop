from django.views.generic.base import ContextMixin

from .models import Category


class MyContextMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.all()
        context['cats'] = cats
        return context


class BaseContextMixin(ContextMixin):
    title = ''

    def get_context_data(self, **kwargs):
        context = super(BaseContextMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context
