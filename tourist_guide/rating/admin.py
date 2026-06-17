from django.contrib import admin

from .models import Rating,RatingImage
# Register your models here.
admin.site.register(Rating)

admin.site.register(RatingImage)