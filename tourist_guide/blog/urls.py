from django.urls import path
from .views import terms ,policy
from . import views

from .views import (
    BlogListAPIView,
    BlogDetailAPIView,
)
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
        

    path("api/blogs/", BlogListAPIView.as_view(), name="blog_list_api"),
    path("blogs/<slug:slug>/", BlogDetailAPIView.as_view(), name="blog_detail_api"),
    
    # HTML Views
    path("blog_list/", views.blog_list, name="blog_list"),
    path("blog_detail/<slug:slug>/", views.blog_detail, name="blog_detail"),

        
#     path(
#         "api/blogs/",
#         BlogListAPIView.as_view(),
#         name="blog_list_api"
#     ),

#     path(
#         "blogs/<slug:slug>/",
#         BlogDetailAPIView.as_view(),
#         name="blog-detail"
#     ),

#     path(
#         "blog_list/",
#         views.blog_list,
#         name="blog_list"
#     ),
    
#     path(
#     "blog_detail/<slug:slug>/",
#     views.blog_detail,
#     name="blog_detail"
# ),
    
    
]