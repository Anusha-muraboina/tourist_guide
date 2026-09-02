from django.contrib import admin
from django.db import models
from django import forms
from tourist.models import (
    TourCategory,
    Tour,
    TourImage,
    TourInclude,
    TourExclude,
    ImportantInformation,
    TourSchedule,
    TourHighlight,
    Amenity,
    TourPricing,
)


# ==========================================
# INLINE MODELS
# ==========================================

class TourImageInline(admin.TabularInline):

    model = TourImage
    extra = 1


class TourScheduleInline(admin.TabularInline):

    model = TourSchedule
    extra = 1

class TourPricingInline(admin.TabularInline):

    model = TourPricing

    extra = 3

    fields = (
        "group_type",
        "group_price",
        "is_active",
    )
# ==========================================
# TOUR CATEGORY ADMIN
# ==========================================

@admin.register(TourCategory)
class TourCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "slot_position",
        "is_active",
        "created_at",
    )

    list_editable = (
        "slot_position",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "slot_position",
    )


# ==========================================
# TOUR INCLUDE ADMIN
# ==========================================

@admin.register(TourInclude)
class TourIncludeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "slot_position",
        "is_active",
    )

    list_editable = (
        "slot_position",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "title",
    )

    ordering = (
        "slot_position",
    )


# ==========================================
# TOUR EXCLUDE ADMIN
# ==========================================

@admin.register(TourExclude)
class TourExcludeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "slot_position",
        "is_active",
    )

    list_editable = (
        "slot_position",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "title",
    )

    ordering = (
        "slot_position",
    )


# ==========================================
# IMPORTANT INFORMATION ADMIN
# ==========================================

@admin.register(ImportantInformation)
class ImportantInformationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "slot_position",
        "is_active",
    )

    list_editable = (
        "slot_position",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "title",
    )

    ordering = (
        "slot_position",
    )


# ==========================================
# TOUR HIGHLIGHT ADMIN
# ==========================================

@admin.register(TourHighlight)
class TourHighlightAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "slot_position",
        "is_active",
    )

    list_editable = (
        "slot_position",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "title",
    )

    ordering = (
        "slot_position",
    )


# ==========================================
# AMENITY ADMIN
# ==========================================

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "icon_class",
        "slot_position",
        "is_active",
    )

    list_editable = (
        "slot_position",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "slot_position",
    )


# ==========================================
# TOUR IMAGE ADMIN
# ==========================================

@admin.register(TourImage)
class TourImageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "tour",
        "is_primary",
        "created_at",
    )

    list_filter = (
        "is_primary",
    )

    search_fields = (
        "tour__title",
    )


# ==========================================
# TOUR SCHEDULE ADMIN
# ==========================================

# @admin.register(TourSchedule)
# class TourScheduleAdmin(admin.ModelAdmin):

#     list_display = (
#         "id",
#         "tour",
#         "start_time",
#         # "end_time",
#         "available_slots",
#         "slot_position",
#         "is_active",
#     )

#     list_filter = (
#         "is_active",
#     )

#     search_fields = (
#         "tour__title",
#     )


@admin.register(TourSchedule)
class TourScheduleAdmin(admin.ModelAdmin):

    formfield_overrides = {

        models.TimeField: {
            "widget": forms.TimeInput(
                attrs={
                    "type": "time",
                    "step": 1800
                },
                format="%H:%M"
            )
        }

    }

    list_display = (
        "id",
        "tour",
        "start_time",
        "available_slots",
        "slot_position",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "tour__title",
    )

    ordering = (
        "slot_position",
    )

# ==========================================
# TOUR ADMIN
# ==========================================

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    # def adult_price(self, obj):

    #     pricing = obj.pricing.filter(
    #         person_type="adult",
    #         is_active=True
    #     ).first()

    #     return pricing.price if pricing else 0

    # adult_price.short_description = "Adult Price"

    list_display = (
        "id",
        "title",
        # "guide",
        "category",
        # "city",
        # "state",
        
         "location",
        # "price",
        # "offer_price",
        "featured",
        "slot_position",
        "is_active",
        "created_at",
        # "adult_price",
    )

    list_editable = (
        "featured",
        "slot_position",
        "is_active",
    )

    list_filter = (
        "tour_type",
        "featured",
        "is_active",
        "free_cancellation",
        "instant_confirmation",
        "pickup_available",
        "wheelchair_accessible",
    )

    # search_fields = (
    #     "title",
    #     "city",
    #     "state",
    #     "country",
    # )
    
    search_fields = (
        "title",
        "location__city",
        "location__state",
        "location__district",
        "location__country",
    )

    ordering = (
        "slot_position",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    filter_horizontal = (
        "includes",
        "excludes",
        "highlights",
        "important_information",
        "amenities",
    )

    inlines = [
        TourImageInline,
        TourScheduleInline,
        TourPricingInline,
    ]

    fieldsets = (

        (
            "Basic Information",
            {
                "fields": (
                    # "guide",
                    "category",
                    "title",
                    "slug",
                    "short_description",
                    "full_description",
                )
            }
        ),

        (
            "Location Information",
            {
                "fields": (
                    # "city",
                    # "state",
                    # "country",
                    # "address",
                    
                    "location",
                    "meeting_point",
                )
            }
        ),

        (
            "Tour Details",
            {
                "fields": (
                    "duration",
                    "language",
                    "tour_type",
                    "max_people",
                    "min_age",
                )
            }
        ),

        # (
        #     "Pricing",
        #     {
        #         "fields": (
        #             "price",
        #             "offer_price",
        #         )
        #     }
        # ),

        (
            "Features",
            {
                "fields": (
                    "free_cancellation",
                    "instant_confirmation",
                    "pickup_available",
                    "wheelchair_accessible",
                    "featured",
                )
            }
        ),

        (
            "Relations",
            {
                "fields": (
                    "includes",
                    "excludes",
                    "highlights",
                    "important_information",
                    "amenities",
                )
            }
        ),

        (
            "Status",
            {
                "fields": (
                    "slot_position",
                    "is_active",
                )
            }
        ),

        (
            "Dates",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            }
        ),

    )
    
    
    
    
    


from django.contrib import admin
from django import forms

from .models import TourSchedule

@admin.register(TourPricing)
class TourPricingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "tour",
        "group_type",
        "group_price",
        "is_active",
    )

    list_editable = (
        "group_price",
        "is_active",
    )

    list_filter = (
        "group_type",
        "is_active",
    )

    search_fields = (
        "tour__title",
    )

    ordering = (
        "tour",
        "group_type",
    )
# =========================
# CUSTOM TIME INPUT
# =========================

# class TourScheduleAdminForm(forms.ModelForm):

#     start_time = forms.TimeField(

#         widget=forms.TimeInput(
#             attrs={
#                 'type': 'time',
#                 'step': 1800
#             },
#             format='%H:%M'
#         ),

#         input_formats=['%H:%M']
#     )

#     class Meta:

#         model = TourSchedule

#         fields = '__all__'


# # =========================
# # ADMIN
# # =========================

# @admin.register(TourSchedule)
# class TourScheduleAdmin(admin.ModelAdmin):

#     form = TourScheduleAdminForm