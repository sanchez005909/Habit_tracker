from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):

    username = None
    email = models.CharField(unique=True, verbose_name='email')
    name = models.CharField(max_length=50, verbose_name='Имя', **NULLABLE)
    chat_id = models.IntegerField(**NULLABLE, verbose_name='chat_id')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
