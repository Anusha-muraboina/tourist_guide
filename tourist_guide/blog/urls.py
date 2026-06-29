from django.urls import path
from .views import terms ,policy
from . import views
urlpatterns = [
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

    # path(
    #     "contact-us/",
    #     views.contact_us,
    #     name="contact_us"
    # ),
]