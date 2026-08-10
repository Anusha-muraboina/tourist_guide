from django.urls import path
from . import views
from .views import (
    BlogCategoryListView,
    BlogCategoryCreateView,
    BlogCategoryUpdateView,
    BlogCategoryDeleteView,
    
    BlogListView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
    
    LocationListView,
    LocationCreateView,
    LocationUpdateView,
    LocationDeleteView,
    
    
    UserListView,
    UserDetailView,
    UserUpdateView,
    
    
    BookingListView,
    BookingDetailView,
    BookingCreateView,
    BookingUpdateView,
    BookingDeleteView,
    BookingStatusUpdateView,
    
)

from .views import (

    CancelReasonListView,
    CancelReasonCreateView,
    CancelReasonUpdateView,
    CancelReasonDeleteView,

)

from .views import (

    BookingCancelCommentListView,

    BookingCancelCommentCreateView,

    BookingCancelCommentUpdateView,

    BookingCancelCommentDeleteView,

)
urlpatterns = [
    # ==========================
    # Dashboard
    # ==========================
    path("dashboard/", views.dashboard, name="dashboard"),

    path("", views.admin_login, name="admin_login"),
    path("login/", views.admin_login, name="admin_login"),
    path("logout/", views.admin_logout, name="admin_logout"),

    # ==========================
    # Tour Category
    # ==========================
    path( "tour-category/", views.TourCategoryListView.as_view(), name="tour_category_list"),
    path( "tour-category/add/", views.TourCategoryCreateView.as_view(), name="tour_category_add"),
    path( "tour-category/<int:pk>/edit/", views.TourCategoryUpdateView.as_view(), name="tour_category_edit"),
    path( "tour-category/<int:pk>/delete/", views.TourCategoryDeleteView.as_view(), name="tour_category_delete"),

    # ==========================
    # Tour Highlight
    # ==========================
    path( "tour-highlight/", views.TourHighlightListView.as_view(),name="tour_highlight_list"),
    path( "tour-highlight/add/",   views.TourHighlightCreateView.as_view(),  name="tour_highlight_add"),
    path( "tour-highlight/<int:pk>/edit/",  views.TourHighlightUpdateView.as_view(),   name="tour_highlight_edit" ),
    path( "tour-highlight/<int:pk>/delete/", views.TourHighlightDeleteView.as_view(), name="tour_highlight_delete"),

    # ==========================
    # Tour Include
    # ==========================
    path( "tour-include/", views.TourIncludeListView.as_view(), name="tour_include_list"),
    path( "tour-include/add/", views.TourIncludeCreateView.as_view(), name="tour_include_add"),
    path( "tour-include/<int:pk>/edit/", views.TourIncludeUpdateView.as_view(), name="tour_include_edit"),
    path( "tour-include/<int:pk>/delete/", views.TourIncludeDeleteView.as_view(), name="tour_include_delete"),

    # ==========================
    # Tour Exclude
    # ==========================
    path( "tour-exclude/", views.TourExcludeListView.as_view(), name="tour_exclude_list"),
    path( "tour-exclude/add/", views.TourExcludeCreateView.as_view(), name="tour_exclude_add"),
    path( "tour-exclude/<int:pk>/edit/", views.TourExcludeUpdateView.as_view(), name="tour_exclude_edit"),
    path( "tour-exclude/<int:pk>/delete/",  views.TourExcludeDeleteView.as_view(),  name="tour_exclude_delete"),

    # ==========================
    # Important Information
    # ==========================
    path(  "important-information/",  views.ImportantInformationListView.as_view(),  name="important_information_list"),
    path(  "important-information/add/", views.ImportantInformationCreateView.as_view(), name="important_information_add"),
    path(  "important-information/<int:pk>/edit/",  views.ImportantInformationUpdateView.as_view(),  name="important_information_edit"),
    path(  "important-information/<int:pk>/delete/",  views.ImportantInformationDeleteView.as_view(),  name="important_information_delete"),

    # ==========================
    # Amenity
    # ==========================
    path( "amenity/", views.AmenityListView.as_view(), name="amenity_list" ),
    path(   "amenity/add/",   views.AmenityCreateView.as_view(),   name="amenity_add"),
    path( "amenity/<int:pk>/edit/", views.AmenityUpdateView.as_view(), name="amenity_edit"),
    path( "amenity/<int:pk>/delete/", views.AmenityDeleteView.as_view(), name="amenity_delete"),
    
    
    path("tour-schedule/",views.TourScheduleListView.as_view(),name="tour_schedule_list",),
    path( "tour-schedule/add/", views.TourScheduleCreateView.as_view(), name="tour_schedule_add",),
    path( "tour-schedule/<int:pk>/edit/", views.TourScheduleUpdateView.as_view(), name="tour_schedule_edit",),
    path(  "tour-schedule/<int:pk>/delete/",  views.TourScheduleDeleteView.as_view(),  name="tour_schedule_delete",),


    #################################################

    path( "tour-pricing/", views.TourPricingListView.as_view(), name="tour_pricing_list",),
    path("tour-pricing/add/",views.TourPricingCreateView.as_view(),name="tour_pricing_add",),
    path("tour-pricing/<int:pk>/edit/",views.TourPricingUpdateView.as_view(),name="tour_pricing_edit",),
    path("tour-pricing/<int:pk>/delete/",views.TourPricingDeleteView.as_view(),name="tour_pricing_delete",),
    
    
    
    # TOUR
    path( "tour/",  views.TourListView.as_view(), name="tour_list",),
    path("tour/add/", views.TourCreateView.as_view(), name="tour_add",),
    path( "tour/<int:pk>/edit/", views.TourUpdateView.as_view(), name="tour_edit",),
    path( "tour/<int:pk>/delete/", views.TourDeleteView.as_view(), name="tour_delete",),
    
    
    # Contact Us
    path("contact-us/",views.ContactUsListView.as_view(),name="contact_us_list"),
    path("contact-us/add/",views.ContactUsCreateView.as_view(),name="contact_us_add"),
    path( "contact-us/<int:pk>/edit/", views.ContactUsUpdateView.as_view(), name="contact_us_edit"),
    path( "contact-us/<int:pk>/delete/", views.ContactUsDeleteView.as_view(), name="contact_us_delete"),
    
    
    path("coupon_list/",views.CouponListView.as_view(),name="coupon_list"),
    path("coupon/add/",views.CouponCreateView.as_view(),name="coupon_add" ),
    path("coupon/<int:pk>/edit/",views.CouponUpdateView.as_view(),name="coupon_edit"),
    path("coupon/<int:pk>/delete/",views.CouponDeleteView.as_view(),name="coupon_delete"),
    
    
    
    path("ratings/",views.RatingListView.as_view(),name="rating_list"),
    path("rating/add/",views.RatingCreateView.as_view(),name="rating_add"),
    path("rating/<int:pk>/edit/", views.RatingUpdateView.as_view(), name="rating_edit"),
    path("rating/<int:pk>/delete/", views.RatingDeleteView.as_view(), name="rating_delete"),



    # ==========================================
    # Blog Category
    # ==========================================

    path( "blog-category/", BlogCategoryListView.as_view(), name="blog_category_list",),
    path("blog-category/create/", BlogCategoryCreateView.as_view(), name="blog_category_create",),
    path("blog-category/<int:pk>/update/",BlogCategoryUpdateView.as_view(),name="blog_category_update",),
    path( "blog-category/<int:pk>/delete/", BlogCategoryDeleteView.as_view(), name="blog_category_delete",),
    
    
    path("blog/",BlogListView.as_view(),name="blog_list",),
    path("blog/create/",BlogCreateView.as_view(),name="blog_create",),
    path( "blog/<int:pk>/update/", BlogUpdateView.as_view(), name="blog_update",),
    path( "blog/<int:pk>/delete/", BlogDeleteView.as_view(), name="blog_delete",),

    path( "cancel-reason/", CancelReasonListView.as_view(), name="cancel_reason_list",),
    path( "cancel-reason/create/", CancelReasonCreateView.as_view(), name="cancel_reason_create",),
    path( "cancel-reason/<int:pk>/update/", CancelReasonUpdateView.as_view(), name="cancel_reason_update",),
    path( "cancel-reason/<int:pk>/delete/", CancelReasonDeleteView.as_view(), name="cancel_reason_delete",),


    path(  "booking-cancel-comment/",  BookingCancelCommentListView.as_view(),  name="booking_cancel_comment_list",),
    path( "booking-cancel-comment/create/", BookingCancelCommentCreateView.as_view(), name="booking_cancel_comment_create",),
    path(  "booking-cancel-comment/<int:pk>/update/",  BookingCancelCommentUpdateView.as_view(),  name="booking_cancel_comment_update",),
    path( "booking-cancel-comment/<int:pk>/delete/", BookingCancelCommentDeleteView.as_view(), name="booking_cancel_comment_delete",),

    path(
        "payment-policy/",
        views.TourPaymentPolicyListView.as_view(),
        name="payment_policy_list",
    ),

    path(
        "payment-policy/add/",
        views.TourPaymentPolicyCreateView.as_view(),
        name="payment_policy_create",
    ),

    path(
        "payment-policy/<int:pk>/edit/",
        views.TourPaymentPolicyUpdateView.as_view(),
        name="payment_policy_update",
    ),

    path( "payment-policy/<int:pk>/delete/", views.TourPaymentPolicyDeleteView.as_view(), name="payment_policy_delete",),
    
    
    path(  "locations/",  LocationListView.as_view(), name="location_list",),

    path("locations/create/",LocationCreateView.as_view(),name="location_create",),

    path( "locations/<int:pk>/update/",LocationUpdateView.as_view(), name="location_update",),

    path("locations/<int:pk>/delete/",LocationDeleteView.as_view(),name="location_delete",),
    
    path(
        "users/",
        UserListView.as_view(),
        name="user_list",
    ),

    path(
        "users/<int:pk>/",
        UserDetailView.as_view(),
        name="user_detail",
    ),

    path(
        "users/<int:pk>/update/",
        UserUpdateView.as_view(),
        name="user_update",
    ),
    
    
    path("bookings/", BookingListView.as_view(), name="booking_list"),
    path("bookings/create/", BookingCreateView.as_view(), name="booking_create"),
    path("bookings/<int:pk>/", BookingDetailView.as_view(), name="booking_detail"),
    path("bookings/<int:pk>/edit/", BookingUpdateView.as_view(), name="booking_update"),
    path("bookings/<int:pk>/delete/", BookingDeleteView.as_view(), name="booking_delete"),
    path("bookings/<int:pk>/status/", BookingStatusUpdateView.as_view(), name="booking_status"),

]