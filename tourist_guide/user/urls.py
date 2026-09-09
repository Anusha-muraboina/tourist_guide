from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    ForgotPasswordAPIView,
    ProfileAPIView,
    LocationListAPIView,
        VerifyRegistrationOTPAPIView,
    ResendRegistrationOTPAPIView,
)
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    # path('forgot_password/', views.forgot_password, name='forgot_password'),
    path(
    'forgot-password/',
    views.forgot_password,
    name='forgot-password-page'
),
    path(
        'api/register/',
        RegisterAPIView.as_view(),
        name='api-register'
    ),
    
        path(
        "api/register/verify-otp/",
        VerifyRegistrationOTPAPIView.as_view(),
        name="verify-registration-otp"
    ),

    path(
        "api/register/resend-otp/",
        ResendRegistrationOTPAPIView.as_view(),
        name="resend-registration-otp"
    ),

    path(
        'api/login/',
        LoginAPIView.as_view(),
        name='api-login'
    ),

    path(
        'api/logout/',
        LogoutAPIView.as_view(),
        name='api-logout'
    ),
    
    path(
        'api/forgot-password/',
        ForgotPasswordAPIView.as_view(),
        name='forgot-password'
    ),
    path( "api/profile/", ProfileAPIView.as_view(), name="profile" ),
    path(
        "profile/",
        views.profile_page,
        name="profile"
    ),
    
    path("api/locations/", LocationListAPIView.as_view(), name="location-list"),
    
    
    path(
        "guides/<int:guide_id>/",
        views.guide_detail,
        name="guide_detail",
    ),
    
    
    

]