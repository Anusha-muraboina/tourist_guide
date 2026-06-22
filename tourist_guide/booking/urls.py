



from django.urls import path
from . import views
from booking.views import ( BookingCreateAPIView,BookingUpdateAPIView ,ApplyCouponAPIView ,BookingListAPIView ,BookingDetailAPIView)

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

]