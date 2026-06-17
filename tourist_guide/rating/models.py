from django.db import models

# Create your models here.
# ratings/models.py

from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe
from django.core.validators import MinValueValidator, MaxValueValidator

from user.models import User
from tourist.models import Tour


class Rating(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ratings"
    )

    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="ratings"
    )

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(5.0)
        ]
    )

    review = models.TextField(
        blank=True,
        null=True,
        help_text="Optional review message"
    )

    anonymous = models.BooleanField(default=False)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)

    # ⭐ Display Stars in Admin
    def display_stars(self):

        full_stars = int(self.rating)

        half_star = (
            self.rating - full_stars
        ) >= 0.5

        empty_stars = (
            5 - full_stars - (1 if half_star else 0)
        )

        full_star_icon = '<i class="fas fa-star text-warning"></i>'

        half_star_icon = '<i class="fas fa-star-half-alt text-warning"></i>'

        empty_star_icon = '<i class="far fa-star text-warning"></i>'

        stars_html = (
            full_star_icon * full_stars +
            (half_star_icon if half_star else '') +
            empty_star_icon * empty_stars
        )

        return mark_safe(stars_html)

    display_stars.short_description = "Stars"

    def __str__(self):

        if self.anonymous:
            return f"Anonymous - {self.rating}★"

        return f"{self.user.email} - {self.rating}★"
    
    
class RatingImage(models.Model):

    rating = models.ForeignKey(
        Rating,
        on_delete=models.CASCADE,
        related_name="images"
    )

    photo = models.ImageField(
        upload_to='rating_images/'
    )

    active = models.BooleanField(default=True)

    def __str__(self):

        return f"Image for {self.rating.tour.title}"