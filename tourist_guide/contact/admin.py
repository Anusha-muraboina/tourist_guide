from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ContactUs


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "phone_number",
        # "subject",
        "is_read",
        "created_at"
    )

    list_filter = (
        "is_read",
        "created_at"
    )

    search_fields = (
        "name",
        "email",
        # "subject"
    )