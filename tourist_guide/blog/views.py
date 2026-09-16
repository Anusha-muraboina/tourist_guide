from django.shortcuts import render

# Create your views here.



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