from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import date


class UserBlogicum(AbstractUser):
    """
    Добавляет к стандартной модели пользователя следующие поля:
    info - информация о себе,
    birthday - дата рождения.
    """

    info = models.TextField('О себе', blank=True)
    birthday = models.DateField('Дата рождения', blank=True, default=date(1900, 1, 1))
