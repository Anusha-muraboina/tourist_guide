from django.contrib import admin


from .models import BlogCategory ,Blog ,PageSEO
# Register your models here.
admin.site.register(BlogCategory)
admin.site.register(Blog)
admin.site.register(PageSEO)
