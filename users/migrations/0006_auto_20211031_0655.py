# Generated by Django 3.2.7 on 2021-10-31 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_userexternprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userexternprofile',
            name='lang',
            field=models.CharField(blank=True, max_length=128, verbose_name='Язык'),
        ),
        migrations.AddField(
            model_name='userexternprofile',
            name='photo',
            field=models.ImageField(blank=True, upload_to='vkphoto/%Y/%m/%d', verbose_name='Фото из вк'),
        ),
    ]