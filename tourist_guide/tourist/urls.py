



from django.urls import path
from . import views
# from . views import terms ,policy
from tourist.views import (
    HomeAPIView,
    TourDetailAPIView,
    CategoryTourAPIView,
    TourListAPIView,
    terms,
    policy,
    FAQListAPIView,
    tour_list
)

from .views import (
    NewsletterSubscriptionAPIView,
    NewsletterUnsubscribeAPIView,
)

urlpatterns = [
    path('', views.home, name='home'),
    

    path('payment-details/', views.payment_details, name='payment_details'),
    
    
     
    path(
        'api/home/',
        HomeAPIView.as_view(),
        name='tour-list-api'
    ),

    path(
        "tours/",
        tour_list,
        name="tourlist"
    ),
    

    path(
        "api/tours/",
        TourListAPIView.as_view(),
        name="tour_list_api"
    ),

    # =========================================
    # TOUR DETAIL API
    # =========================================

    path(
        'api/tours/<slug:slug>/',
        TourDetailAPIView.as_view(),
        name='tour-detail-api'
    ),
    
    path(
    'tour-details/<slug:slug>/',
    views.tour_details,
    name='tour_details'
),
    
    path("faqs/", FAQListAPIView.as_view(), name="faq-list"),
    
    path(
        "api/categories/",
        CategoryTourAPIView.as_view()
    ),
    
    
    
    path(
        "terms/",
        terms,
        name="terms"
    ),

    path(
        "policy/",
        policy,
        name="policy"
    ),
    
    path(
        "about-us/",
        views.about_us,
        name="about_us"
    ),
    
        # Newsletter
    path(
        "api/newsletter/subscribe/",
        NewsletterSubscriptionAPIView.as_view(),
        name="newsletter-subscribe",
    ),

    path(
        "api/newsletter/unsubscribe/",
        NewsletterUnsubscribeAPIView.as_view(),
        name="newsletter-unsubscribe",
    ),
   
]