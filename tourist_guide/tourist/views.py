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


# class HomeListAPIView(
#     generics.ListAPIView
# ):

#     serializer_class = TourListSerializer

#     permission_classes = [AllowAny]

#     queryset = (
#         Tour.objects
#         .filter(
#             is_active=True
#         )
#         .select_related(
#             "category",
#             "guide",
#         )
#         .prefetch_related(
#             "images",
#             "pricing"
#         )
#         .order_by(
#             "slot_position",
#             "-id",
#         )
#     )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from tourist.models import Tour
from tourist.serializers import TourListSerializer



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q

from tourist.models import Tour
from tourist.serializers import TourListSerializer

from rating.serializers import RatingSerializer
class HomeAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        search = request.GET.get("search")

        tours = (
            Tour.objects
            .filter(is_active=True)
            .prefetch_related(
                "images",
                "pricing"
            )
        )

        # =====================
        # SEARCH
        # =====================

        if search:

            tours = tours.filter(

                Q(title__icontains=search) |

                Q(short_description__icontains=search) |

                Q(city__icontains=search) |

                Q(state__icontains=search) |

                Q(category__name__icontains=search)

            )

        # =====================
        # TOURS
        # =====================

        tours_data = TourListSerializer(
            tours[:20],
            many=True,
            context={
                "request": request
            }
        ).data




        #         # =====================
#         # UNFORGETTABLE
#         # =====================

        unforgettable = (
            Tour.objects
            .filter(
                featured=True,
                is_active=True
            )
            .prefetch_related(
                "images",
                "pricing"
            )[:8]
        )

        unforgettable_data = (
            TourListSerializer(
                unforgettable,
                many=True,
                context={
                    "request": request
                }
            ).data
        )





        # =====================
        # DESTINATIONS
        # =====================

        destinations = []

        states = (
            Tour.objects
            .filter(is_active=True)
            .values_list(
                "state",
                flat=True
            )
            .distinct()
        )

        for state in states:

            first_tour = (
                Tour.objects
                .filter(
                    state=state,
                    is_active=True
                )
                .prefetch_related(
                    "images"
                )
                .first()
            )

            image = None

            if (
                first_tour and
                first_tour.images.first()
            ):

                image = request.build_absolute_uri(
                    first_tour.images.first().image.url
                )

            destinations.append({

                "state": state,

                "image": image

            })

        return Response({

            "tours": tours_data,

            "destinations": destinations,
                        "unforgettable":
                unforgettable_data


        })
# class HomeAPIView(APIView):

#     permission_classes = [AllowAny]

#     def get(self, request):

#         # =====================
#         # CONTINUE PLANNING
#         # =====================

#         continue_planning = (
#             Tour.objects
#             .filter(
#                 is_active=True
#             )
#             .prefetch_related(
#                 "images",
#                 "pricing"
#             )[:6]
#         )

#         continue_planning_data = (
#             TourListSerializer(
#                 continue_planning,
#                 many=True,
#                 context={
#                     "request": request
#                 }
#             ).data
#         )

#         # =====================
#         # UNFORGETTABLE
#         # =====================

#         unforgettable = (
#             Tour.objects
#             .filter(
#                 featured=True,
#                 is_active=True
#             )
#             .prefetch_related(
#                 "images",
#                 "pricing"
#             )[:8]
#         )

#         unforgettable_data = (
#             TourListSerializer(
#                 unforgettable,
#                 many=True,
#                 context={
#                     "request": request
#                 }
#             ).data
#         )

#         # =====================
#         # STATES
#         # =====================

#         destinations = []

#         states = (
#             Tour.objects
#             .filter(
#                 is_active=True
#             )
#             .values_list(
#                 "state",
#                 flat=True
#             )
#             .distinct()
#         )

#         for state in states:

#             tour = (
#                 Tour.objects
#                 .filter(
#                     state=state,
#                     is_active=True
#                 )
#                 .prefetch_related(
#                     "images"
#                 )
#                 .first()
#             )

#             image = None

#             if (
#                 tour and
#                 tour.images.first()
#             ):

#                 image = request.build_absolute_uri(
#                     tour.images.first().image.url
#                 )

#             destinations.append({

#                 "state": state,

#                 "image": image

#             })

#         return Response({

#             "tours":
#                 continue_planning_data,

#             "destinations":
#                 destinations,

#             "unforgettable":
#                 unforgettable_data

#         })

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
            # "guide",
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





from rest_framework.views import APIView
from rest_framework.response import Response

from tourist.models import TourCategory
from tourist.serializers import CategorySerializer

from rest_framework.views import APIView
from rest_framework.response import Response

from tourist.models import (
    TourCategory
)


class CategoryTourAPIView(APIView):

    def get(self, request):

        response_data = []

        categories = (
            TourCategory.objects
            .filter(is_active=True)
            .prefetch_related(
                "tours__images",
                "tours__pricing"
            )
            .order_by("name")
        )

        for category in categories:

            tours_data = []

            tours = category.tours.filter(
                is_active=True
            )

            for tour in tours:

                image = tour.images.first()

                adult_price = 0

                pricing = tour.pricing.filter(
                    person_type="adult",
                    is_active=True
                ).first()

                if pricing:
                    adult_price = pricing.price

                tours_data.append({

                    "id":
                        tour.id,

                    "title":
                        tour.title,

                    "slug":
                        tour.slug,

                    "adult_price":
                        float(
                            adult_price
                        ),

                    "image":
                        request.build_absolute_uri(
                            image.image.url
                        )
                        if image
                        else None

                })

            response_data.append({

                "id":
                    category.id,

                "name":
                    category.name,

                "tours":
                    tours_data

            })

        return Response(
            response_data
        )