


from django.urls import path
from .views import ContactUsAPIView,contact

urlpatterns = [

    path(
        "contact-us/",
        ContactUsAPIView.as_view(),
        name="contact-us-api"
    ),
    
    path(
        "contact/",
        contact,
        name="contact"
    
    ),
    

]

