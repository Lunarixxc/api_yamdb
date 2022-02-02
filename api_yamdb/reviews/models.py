from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODER = 'moderator'
ADMIN = 'admin'

ROLES = [
    (USER, 'Пользователь'),
    (MODER, 'Модератор'),
    (ADMIN, 'Админ'),
]


class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.TextField(
        'Роль',
        choices=ROLES,
        default=USER,
    )
