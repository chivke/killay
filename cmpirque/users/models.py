from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, UserManager


class User(AbstractUser):
    '''
    Default user cmpirque.
    '''

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    objects = UserManager()

    def __str__(self):
        is_admin = " (admin)" if self.is_superuser else ""
        return f"{self.username}{is_admin}"

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
