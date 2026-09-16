from django.urls import path
# from .views import terms ,policy
from . import views

from .views import (
    BlogListAPIView,
    BlogDetailAPIView,
)
urlpatterns = [


    path("api/blogs/", BlogListAPIView.as_view(), name="blog_list_api"),
    path("blogs/<slug:slug>/", BlogDetailAPIView.as_view(), name="blog_detail_api"),
    
    # HTML Views
    path("blog_list/", views.blog_list, name="bloglisting"),
    path("<slug:slug>/", views.blog_detail, name="blog_detail"),

        
    
    
]