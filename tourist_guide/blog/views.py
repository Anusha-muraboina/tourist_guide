from django.shortcuts import render

# Create your views here.




from django.shortcuts import render

def terms(request):
    return render(
        request,
        "pages/terms_condition.html"
    )
    
def policy(request):
    return render(
        request,
        "pages/policy.html"
    )
    
from django.shortcuts import render

def about_us(request):
    return render(
        request,
        "pages/about_us.html"
    )


# def contact_us(request):
#     return render(
#         request,
#         "pages/contact_us.html"
#     )




# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from blog.models import Blog
# from .serializers import BlogListSerializer


# class BlogListAPIView(APIView):

#     def get(self, request):

#         search = request.GET.get("search")
#         category = request.GET.get("category")
#         featured = request.GET.get("featured")

#         blogs = Blog.objects.filter(
#             is_active=True
#         ).select_related(
#             "category"
#         )

#         if search:
#             blogs = blogs.filter(
#                 title__icontains=search
#             )

#         if category:
#             blogs = blogs.filter(
#                 category__slug=category
#             )

#         if featured == "1":
#             blogs = blogs.filter(
#                 featured=True
#             )

#         serializer = BlogListSerializer(
#             blogs,
#             many=True,
#             context={
#                 "request": request
#             }
#         )

#         return Response({

#             "success": True,

#             "count": blogs.count(),

#             "data": serializer.data

#         })
        
        

# from blog.models import Blog


# class BlogDeleteAPIView(APIView):

#     def delete(self, request, blog_id):

#         try:

#             blog = Blog.objects.get(
#                 id=blog_id
#             )

#         except Blog.DoesNotExist:

#             return Response({

#                 "success": False,

#                 "message": "Blog not found"

#             }, status=status.HTTP_404_NOT_FOUND)

#         blog.delete()

#         return Response({

#             "success": True,

#             "message": "Blog deleted successfully"

#         }, status=status.HTTP_200_OK)



from django.db.models import Q, F
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Blog
from .serializers import (
    BlogListSerializer,
    BlogDetailSerializer
)


class BlogListAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        search = request.GET.get("search")
        category = request.GET.get("category")
        featured = request.GET.get("featured")

        blogs = Blog.objects.filter(
            is_active=True
        ).select_related("category")

        if category:
            blogs = blogs.filter(
                category__slug=category
            )

        if featured == "true":
            blogs = blogs.filter(
                featured=True
            )

        if search:
            blogs = blogs.filter(
                Q(title__icontains=search) |
                Q(short_description__icontains=search)
            )

        serializer = BlogListSerializer(
            blogs,
            many=True,
            context={"request": request}
        )

        return Response({
            "success": True,
            "count": blogs.count(),
            "results": serializer.data
        })


class BlogDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, slug):

        blog = Blog.objects.select_related(
            "category"
        ).filter(
            slug=slug,
            is_active=True
        ).first()

        if not blog:
            return Response({
                "success": False,
                "message": "Blog not found."
            }, status=404)

        Blog.objects.filter(
            id=blog.id
        ).update(
            views=F("views") + 1
        )

        blog.refresh_from_db()

        serializer = BlogDetailSerializer(
            blog,
            context={"request": request}
        )

        return Response({
            "success": True,
            "data": serializer.data
        })
        
        


def blog_list(request):
    return render(
        request,
        "blog/list.html"
    )
    
def blog_detail(request, slug):
    return render(
        request,
        "blog/detail.html"
    )