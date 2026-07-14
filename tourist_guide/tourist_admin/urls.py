from django.urls import path
from . import views

urlpatterns = [

    # ==========================
    # Dashboard
    # ==========================
    path("dashboard/", views.dashboard, name="dashboard"),


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
    path(  "tour-highlight/add/",   views.TourHighlightCreateView.as_view(),  name="tour_highlight_add"),
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
    path(  "tour-exclude/<int:pk>/delete/",  views.TourExcludeDeleteView.as_view(),  name="tour_exclude_delete"),


    # ==========================
    # Important Information
    # ==========================
    path(  "important-information/",  views.ImportantInformationListView.as_view(),  name="important_information_list"),
    path( "important-information/add/", views.ImportantInformationCreateView.as_view(), name="important_information_add"),
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


    



]