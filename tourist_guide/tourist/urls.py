



from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path(
    'tour-details/',
    views.tour_details,
    name='tour_details'
),
    path('payment-details/', views.payment_details, name='payment_details'),
    
]