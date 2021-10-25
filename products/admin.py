from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Products, Category


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'desc', 'price', 'get_image', 'created_at', 'updated_at',
                    'category', 'is_published')
    list_display_links = ('title', 'id')
    search_fields = ('title', 'desc')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'image', 'title', 'category')
    fields = ('title', 'category', 'desc', 'price', 'image', 'get_image', 'created_at',
    'updated_at', 'is_published')
    readonly_fields = ('get_image', 'created_at', 'updated_at')

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="75"')

    get_image.short_description = 'Изображение'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')
    list_display_links = ('title', 'image')
    search_fields = ('title',)


admin.site.register(Products, ProductsAdmin)
admin.site.register(Category, CategoryAdmin)
