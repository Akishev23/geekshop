from django.contrib import admin

from .models import Products, Category


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'desc', 'price', 'image', 'created_at', 'updated_at',
                    'category', 'is_published')
    list_display_links = ('title', 'id')
    search_fields = ('title', 'desc')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'image', 'title', 'category')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')
    list_display_links = ('title', 'image')
    search_fields = ('title', )


admin.site.register(Products, ProductsAdmin)
admin.site.register(Category, CategoryAdmin)
