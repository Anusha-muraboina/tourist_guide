



from django.urls import path
from . import views

from tourist.views import (
    HomeAPIView,
    TourDetailAPIView,
    CategoryTourAPIView
)
urlpatterns = [
    path('', views.home, name='home'),
    

    path('payment-details/', views.payment_details, name='payment_details'),
    
    
     
    path(
        'api/home/',
        HomeAPIView.as_view(),
        name='tour-list-api'
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
    
    path(
        "api/categories/",
        CategoryTourAPIView.as_view()
    ),
    
]