from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    username = None

    ROLE_CHOICES = (
        ('tourist', 'Tourist'),
        ('guide', 'Guide'),
    )

    email = models.EmailField(unique=True)

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email