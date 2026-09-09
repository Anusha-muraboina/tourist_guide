from django.contrib import admin

from user.models import User,Location,GuideProfile

# Register your models here.
admin.site.register(User)

admin.site.register(Location)

admin.site.register(GuideProfile)