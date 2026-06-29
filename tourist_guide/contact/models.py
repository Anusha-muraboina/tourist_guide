from django.db import models

# Create your models here.
from django.db import models


class ContactUs(models.Model):

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    # subject = models.CharField(
    #     max_length=200
    # )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.name}"
        )