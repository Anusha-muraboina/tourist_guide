from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    # username = None
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )
    ROLE_CHOICES = (
        ('tourist', 'Tourist'),
        ('guide', 'Guide'),
    )
    username = models.CharField(
        max_length=150,
        unique=True
    )

    email = models.EmailField(unique=True)

    phone_number = models.CharField(
        max_length=15,
        # blank=True,
        # null=True
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
    
    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )


    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email