from django.db import models
from django.contrib.auth.models import AbstractUser


from django.db import models
from django.contrib.auth.models import AbstractUser


class Location(models.Model):
    country = models.CharField(
        max_length=100,
        default="India"
    )

    state = models.CharField(
        max_length=100
    )

    district = models.CharField(
        max_length=100
    )

    city = models.CharField(
        max_length=100
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["state", "district", "city"]
        unique_together = ("state", "district", "city")

    def __str__(self):
        return f"{self.city}, {self.district}, {self.state}"


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
        ('admin' , 'Admin'),
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

    # location = models.CharField(
    #     max_length=255,
    #     blank=True,
    #     null=True
    # )
    
    locations = models.ManyToManyField(
        Location,
        blank=True,
        related_name="guides"
    )
    
    # state = models.CharField(
    #     max_length=100,
    #     blank=True,
    #     null=True
    # )

    # country = models.CharField(
    #     max_length=100,
    #     default="India",
    #     null =True,
    #     blank=True
    # )


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