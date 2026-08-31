from django.contrib import admin

# Register your models here.
# bookings/admin.py

from django.contrib import admin
from .models import (
    Booking,
    BlockedTourDate,
    TourPaymentPolicy,
    Invoice,
    CancelReason,
    BookingCancelComment,
)


# =========================
# BOOKING ADMIN
# =========================

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "booking_id",
        "guest_name",
        "tour",
        "tour_date",
        "payment_method",
        "payment_status",
        "status",
        "total_amount",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_status",
        "payment_method",
        "tour_date",
        "created_at",
    )

    search_fields = (
        "booking_id",
        "guest_name",
        "guest_email",
        "guest_phone",
        "payment_id",
        "transaction_id",
    )

    readonly_fields = (
        "booking_id",
        "created_at",
        "advance_amount",
        "remaining_amount",
    )

    ordering = ("-created_at",)

    fieldsets = (

        ("Booking Info", {
            "fields": (
                "booking_id",
                "tour",
                "user",
                "status",
            )
        }),

        ("Guest Details", {
            "fields": (
                "guest_name",
                "guest_email",
                "guest_phone",
            )
        }),

        ("Travellers", {
            "fields": (
                # "adults",
                # "children",
                # "infants",
                "pricing",
            )
        }),

        ("Tour Schedule", {
            "fields": (
                "tour_date",
                "tour_time",
                "special_requests",
            )
        }),

        ("Pricing", {
            "fields": (
                "sub_total",
                "discount_amount",
                "tax_amount",
                "total_amount",
                "advance_amount",
                "remaining_amount",
            )
        }),

        ("Coupon", {
            "fields": (
                "coupon_applied",
            )
        }),

        ("Payment Details", {
            "fields": (
                "payment_method",
                "payment_status",
                "payment_id",
                "transaction_id",
            )
        }),

        ("Cancellation", {
            "fields": (
                "cancelled_at",
                "cancelled_by",
            )
        }),

        ("Dates", {
            "fields": (
                "created_at",
            )
        }),
    )


# =========================
# BLOCKED TOUR DATE ADMIN
# =========================

@admin.register(BlockedTourDate)
class BlockedTourDateAdmin(admin.ModelAdmin):

    list_display = (
        "tour",
        "blocked_date",
        "reason",
        "created_at",
    )

    list_filter = (
        "blocked_date",
        "created_at",
    )

    search_fields = (
        "tour__title",
        "reason",
    )

    ordering = ("-blocked_date",)


# =========================
# TOUR PAYMENT POLICY ADMIN
# =========================

@admin.register(TourPaymentPolicy)
class TourPaymentPolicyAdmin(admin.ModelAdmin):

    list_display = (
        "tour",
        "allow_pay_at_location",
        "allow_partial_payment",
        "allow_full_payment",
    )

    search_fields = (
        "tour__title",
    )


# =========================
# INVOICE ADMIN
# =========================

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    list_display = (
        "invoice_id",
        "booking",
        "invoice_date",
        "is_active",
    )

    list_filter = (
        "is_active",
        "invoice_date",
    )

    search_fields = (
        "invoice_id",
        "booking__booking_id",
    )

    readonly_fields = (
        "invoice_id",
        "invoice_date",
    )


# =========================
# CANCEL REASON ADMIN
# =========================

@admin.register(CancelReason)
class CancelReasonAdmin(admin.ModelAdmin):

    list_display = (
        "reason",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "reason",
    )


# =========================
# BOOKING CANCEL COMMENT ADMIN
# =========================

@admin.register(BookingCancelComment)
class BookingCancelCommentAdmin(admin.ModelAdmin):

    list_display = (
        "booking",
        "user",
        "reason",
        "created_at",
    )

    list_filter = (
        "created_at",
        "reason",
    )

    search_fields = (
        "booking__booking_id",
        "user__email",
        "comment",
    )

    readonly_fields = (
        "created_at",
    )