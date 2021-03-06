from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Категория товара')
    image = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='Изображение')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('get_cat', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Products(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование товара', db_index=True)
    desc = models.TextField(blank=True, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    is_published = models.BooleanField(default=True, verbose_name='Флаг публикации')
    quantity = models.PositiveIntegerField(default=10)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True,
                                 verbose_name='Категория')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['id']
