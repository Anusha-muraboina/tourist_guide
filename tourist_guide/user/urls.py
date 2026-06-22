from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    ForgotPasswordAPIView,
    ProfileAPIView
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


]