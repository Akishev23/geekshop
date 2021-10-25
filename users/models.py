from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    image = models.ImageField(upload_to='user_image', blank=True)

    def get_absolut_url(self):
        return reverse('users:profile', args=[self.pk])
