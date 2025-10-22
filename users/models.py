from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_USER = 'user'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = [
        (ROLE_USER, 'User'),
        (ROLE_ADMIN, 'Admin'),
    ]

    email = models.EmailField(unique=True, blank=False)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_USER,
        help_text="Роль пользователя в системе"
    )

    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def __str__(self):
        return self.username