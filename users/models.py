from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.timezone import now

NULL_INSTALL = {'null': 'True', 'blank': 'True'}


class User(AbstractUser):
    image = models.ImageField(upload_to='user_image', blank=True)
    age = models.PositiveIntegerField(default=18)

    activation_key = models.CharField(max_length=128, **NULL_INSTALL)
    activation_key_created = models.DateTimeField(auto_now_add=True, **NULL_INSTALL)

    def get_absolut_url(self):
        return reverse('users:profile', args=[self.pk])

    def is_activation_key_expired(self):
        if now() <= self.activation_key_created + timedelta(hours=48):
            return False
        return True
