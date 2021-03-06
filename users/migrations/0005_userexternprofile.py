# Generated by Django 3.2.7 on 2021-10-31 01:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20211030_0050'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExternProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagline', models.CharField(blank=True, max_length=128, verbose_name='Теги')),
                ('about', models.TextField(blank=True, null=True, verbose_name='О себе')),
                ('gender', models.CharField(blank=True, choices=[('M', 'М'), ('W', 'Ж')], max_length=2, verbose_name='Пол')),
                ('email', models.CharField(blank=True, max_length=128)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
