from django.db import models

# Create your models here.




from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class BlogCategory(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    slot_position = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["slot_position"]

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =====================================
# BLOG
# =====================================

class Blog(models.Model):

    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blogs"
    )

    title = models.CharField(
        max_length=250
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    short_description = models.TextField(
        help_text="Short summary"
    )

    description = RichTextField()

    image = models.ImageField(
        upload_to="blogs/"
    )

    author = models.CharField(
        max_length=100,
        default="Admin"
    )

    reading_time = models.PositiveIntegerField(
        default=5,
        help_text="Minutes"
    )

    views = models.PositiveIntegerField(
        default=0
    )

    featured = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    slot_position = models.PositiveIntegerField(
        default=0
    )

    # SEO

    meta_title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    meta_description = models.TextField(
        blank=True,
        null=True
    )

    meta_keywords = models.TextField(
        blank=True,
        null=True,
        help_text="Comma separated keywords"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "slot_position",
            "-created_at"
        ]

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title