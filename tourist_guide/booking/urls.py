



from django.urls import path
from . import views
from booking.views import ( BookingCreateAPIView,BookingUpdateAPIView ,ApplyCouponAPIView ,BookingListAPIView ,BookingDetailAPIView)
from booking.views import (
    CreateRazorpayOrderAPIView,
    VerifyAndCreateBookingAPIView,
    RazorpayWebhookAPIView
)

urlpatterns = [
    path('booking/', views.booking, name='booking'),
    path( "create-booking/", BookingCreateAPIView.as_view(), name="create_booking" ),
    
    path(
    "booking-success/<int:booking_id>/",
    views.booking_success,
    name="booking_success"
),

    path(
    "apply-coupon/",
    ApplyCouponAPIView.as_view(),
    name="apply_coupon"
),
    
    path(
    "update-booking/<int:booking_id>/",
    BookingUpdateAPIView.as_view(),
    name="update_booking"
),

    path(
    "apply-coupon/",
    ApplyCouponAPIView.as_view(),
    name="apply_coupon"
),
    
    
    path(
        "api/booking-list/",
        BookingListAPIView.as_view(),
        name="booking-list"
    ),

    path(
        "api/booking-detail/<int:booking_id>/",
        BookingDetailAPIView.as_view(),
        name="booking-detail"
    ),
    
    
    path(
    "my-bookings/",
    views.my_bookings,
    name="my-bookings"
    ),
    
    path(
        "invoice/<str:booking_id>/",
        views.view_invoice,
        name="view_invoice"
    ),

    path(
        "cancel-booking/<str:booking_id>/",
        views.CancelBookingAPI.as_view(),
    ),
    
    path(
        "cancel-reasons/",
        views.CancelReasonListAPI.as_view(),
    ),
    
    path(
        "cancel_booking_page/<str:booking_id>/",
        views.cancel_booking_page  ,name="cancel_booking_page"
    ),
    
    path("create-razorpay-order/", CreateRazorpayOrderAPIView.as_view()),
    path("verify-and-create-booking/", VerifyAndCreateBookingAPIView.as_view()),
    path("payments/webhook/", RazorpayWebhookAPIView.as_view()),
]