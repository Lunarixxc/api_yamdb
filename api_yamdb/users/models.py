from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = [
    ("user", "user"),
    ("moderator", "moderator"),
    ("admin", "admin"),
]


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.TextField(
        'Роль',
        choices=ROLES,
        default=ROLES[0],
    )


