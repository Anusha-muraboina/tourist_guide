from django.contrib import admin

from user.models import User,Location,GuideProfile

# Register your models here.
admin.site.register(User)

admin.site.register(Location)

admin.site.register(GuideProfile)



from django.contrib import admin

from .models import NewsletterSubscription


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "is_active",
        "subscribed_at",
        "unsubscribed_at",
    )

    list_filter = (
        "is_active",
        "subscribed_at",
    )

    search_fields = (
        "email",
    )

    readonly_fields = (
        "subscribed_at",
        "unsubscribed_at",
    )

    ordering = (
        "-subscribed_at",
    )