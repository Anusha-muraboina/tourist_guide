from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
    # return HttpResponse("Welcome to Tourist Guide")
    # render(request )
    return render(request, 'home.html')



def tour_details(request):

    return render(
        request,
        'detailpage.html'
    )


def payment_details(request):

    return render(
        request,
        'payment.html'
    )
    
    
# tours/api/views.py

from rest_framework import generics
from rest_framework.permissions import AllowAny

from tourist.models import Tour

from tourist.serializers import (
    TourListSerializer,
    TourDetailSerializer,
)


# =========================================
# TOUR LIST API
# =========================================

class HomeListAPIView(
    generics.ListAPIView
):

    serializer_class = TourListSerializer

    permission_classes = [AllowAny]

    queryset = Tour.objects.filter(
        is_active=True
    ).prefetch_related(
        "images"
    ).order_by("-id")



# views.py

# from django.shortcuts import render


# def home(request):

#     tours = Tour.objects.filter(
#         is_active=True
#     ).prefetch_related(
#         "images"
#     ).order_by("-id")

#     context = {

#         "tours": tours

#     }

#     return render(
#         request,
#         "home.html",
#         context
#     )

# =========================================
# TOUR DETAIL API
# =========================================
# tours/api/views.py

from rest_framework import generics
from rest_framework.permissions import AllowAny

from tourist.models import Tour

from .serializers import (
    TourListSerializer,
    TourDetailSerializer,
)


# =========================================
# HOME TOUR LIST API
# =========================================


class HomeListAPIView(
    generics.ListAPIView
):

    serializer_class = TourListSerializer

    permission_classes = [AllowAny]

    queryset = (
        Tour.objects
        .filter(
            is_active=True
        )
        .select_related(
            "category",
            "guide",
        )
        .prefetch_related(
            "images",
            "pricing"
        )
        .order_by(
            "slot_position",
            "-id",
        )
    )



# =========================================
# TOUR DETAIL API
# =========================================

class TourDetailAPIView(
    generics.RetrieveAPIView
):

    serializer_class = TourDetailSerializer

    permission_classes = [AllowAny]

    lookup_field = "slug"

    queryset = (
        Tour.objects
        .filter(
            is_active=True
        )
        .select_related(
            "category",
            "guide",
        )
        .prefetch_related(

            "images",

            "highlights",

            "includes",

            "excludes",

            "important_information",

            "schedules",

            "amenities",
            "pricing",

        )
    )
def tour_details(request, slug):

    return render(
        request,
        "detailpage.html",
        {
            "slug": slug
        }
    )
# def tour_details(request):

#     return render(
#         request,
#         'detailpage.html'
#     )





