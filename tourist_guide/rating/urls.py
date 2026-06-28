
from django.urls import path
from . import views
from .views import AddRatingAPIView
urlpatterns = [
    path('rating/', views.rating, name='rating'),
    
    path(
        "add-rating/",
        AddRatingAPIView.as_view(),
        name="add-rating"
    ),
]