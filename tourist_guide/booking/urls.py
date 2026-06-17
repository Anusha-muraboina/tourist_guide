



from django.urls import path
from . import views
from booking.views import ( BookingCreateAPIView,BookingUpdateAPIView ,ApplyCouponAPIView )

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
]