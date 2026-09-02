from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from rest_framework import generics
from rest_framework.permissions import AllowAny

from tourist.models import Tour

from .serializers import (
    TourListSerializer,
    TourDetailSerializer,
)



from tourist.serializers import CategorySerializer
from tourist.models import (
    TourCategory
)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from tourist.models import Tour
from tourist.serializers import TourListSerializer


from django.db.models import Q
from rating.serializers import RatingSerializer


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



class HomeAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        search = request.GET.get("search")

        tours = (
            Tour.objects
            .filter(is_active=True)
            .select_related("location")
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
                
                Q(location__city__icontains=search) |
                Q(location__state__icontains=search) |
                Q(location__district__icontains=search) |

                # Q(city__icontains=search) |

                # Q(state__icontains=search) |

                Q(category__name__icontains=search)

            )

        # =====================
        # TOURS
        # =====================

        tours_data = TourListSerializer(
            tours[:4],
            many=True,
            context={
                "request": request
            }
        ).data

        recent_tours = (
            Tour.objects
            .filter(
                is_active=True
            )
            .select_related(
                "location",
                "category"
            )
            .prefetch_related(
                "images",
                "pricing"
            )
            .order_by("-created_at")[:3]
        )

        recent_tours_data = TourListSerializer(
            recent_tours,
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
            .filter(is_active=True , location__isnull=False)
            .values_list("location__state", flat=True)
            .distinct()
        )

        for state in states:

            first_tour = (
                Tour.objects
                .filter(
                    location__state=state,
                    is_active=True
                )
                .select_related("location")
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
            
            "recent_tours": recent_tours_data,

            "destinations": destinations,
                        "unforgettable":
                unforgettable_data


        })






#  tour list api





class TourListAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        search = request.GET.get("search", "").strip()
        location = request.GET.get("location", "").strip()
        offset = int(request.GET.get("offset", 0))
        limit = 3

        # ==========================================
        # BASE QUERY
        # ==========================================

        tours = (
            Tour.objects
            .filter(is_active=True)
            .select_related(
                "location",
                "category"
            )
            .prefetch_related(
                "images",
                "pricing"
            )
            .order_by("-created_at")
        )

        # ==========================================
        # SEARCH
        # ==========================================

        if search:

            tours = tours.filter(

                Q(title__icontains=search) |

                Q(short_description__icontains=search) |

                Q(location__city__icontains=search) |

                Q(location__state__icontains=search) |

                Q(location__district__icontains=search) |

                Q(category__name__icontains=search)

            ).distinct()

        # ==========================================
        # LOCATION FILTER
        # ==========================================

        if location:

            tours = tours.filter(
                location_id=location
            )

        # ==========================================
        # TOTAL COUNT
        # ==========================================

        total_count = tours.count()

        # ==========================================
        # PAGINATION
        # ==========================================

        paginated_tours = tours[
            offset:offset + limit
        ]

        serializer = TourListSerializer(
            paginated_tours,
            many=True,
            context={
                "request": request
            }
        )

        # ==========================================
        # LOCATIONS DROPDOWN
        # ==========================================

        locations = (
            Tour.objects
            .filter(
                is_active=True,
                location__isnull=False
            )
            .select_related("location")
            .values(
                "location__id",
                "location__city",
                "location__district",
                "location__state",
                "location__country"
            )
            .distinct()
            .order_by(
                "location__state",
                "location__city"
            )
        )

        location_data = []

        for loc in locations:

            location_data.append({

                "id": loc["location__id"],

                "city": loc["location__city"],

                "district": loc["location__district"],

                "state": loc["location__state"],

                "country": loc["location__country"],

            })

        # ==========================================
        # HAS MORE
        # ==========================================

        next_offset = offset + limit

        has_more = next_offset < total_count

        # ==========================================
        # RESPONSE
        # ==========================================

        return Response({

            "success": True,

            "count": total_count,

            "offset": offset,

            "limit": limit,

            "next_offset": next_offset,

            "has_more": has_more,

            "locations": location_data,

            "results": serializer.data,

        })
        
        

def tour_list(request):
    return render(
        request,
        "listing.html"
    )




# =========================================
# TOUR DETAIL API
# =========================================



class TourDetailAPIView(generics.RetrieveAPIView):

    serializer_class = TourDetailSerializer
    permission_classes = [AllowAny]

    lookup_field = "slug"

    queryset = (
        Tour.objects
        .filter(is_active=True)
        .select_related(
            "category",
            "location",
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

# class TourDetailAPIView(
#     generics.RetrieveAPIView
# ):

#     serializer_class = TourDetailSerializer

#     permission_classes = [AllowAny]

#     lookup_field = "slug"

#     queryset = (
#         Tour.objects
#         .filter(
#             is_active=True
#         )
#         .select_related(
#             "category",
#             # "guide",
#         )
#         .prefetch_related(

#             "images",

#             "highlights",

#             "includes",

#             "excludes",

#             "important_information",

#             "schedules",

#             "amenities",
#             "pricing",

#         )
#     )
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












class CategoryTourAPIView(APIView):

    permission_classes = [AllowAny]

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

                # ==========================================
                # GROUP PRICING
                # ==========================================

                pricing_data = []

                pricing = tour.pricing.filter(
                    is_active=True
                ).order_by("id")

                for price in pricing:

                    pricing_data.append({

                        "id": price.id,

                        "group_type":
                            price.group_type,

                        "group_members":
                            price.group_members,

                        "group_price":
                            float(
                                price.group_price
                            ),

                        "label":
                            price.get_group_type_display(),

                    })

                # ==========================================
                # TOUR DATA
                # ==========================================

                tours_data.append({
                    

                    "id":
                        tour.id,

                    "title":
                        tour.title,

                    "slug":
                        tour.slug,

                    "pricing":
                        pricing_data,

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

# class CategoryTourAPIView(APIView):

#     def get(self, request):

#         response_data = []

#         categories = (
#             TourCategory.objects
#             .filter(is_active=True)
#             .prefetch_related(
#                 "tours__images",
#                 "tours__pricing"
#             )
#             .order_by("name")
#         )

#         for category in categories:

#             tours_data = []

#             tours = category.tours.filter(
#                 is_active=True
#             )

#             for tour in tours:

#                 image = tour.images.first()

#                 adult_price = 0

#                 pricing = tour.pricing.filter(
#                     person_type="adult",
#                     is_active=True
#                 ).first()

#                 if pricing:
#                     adult_price = pricing.price

#                 tours_data.append({

#                     "id":
#                         tour.id,

#                     "title":
#                         tour.title,

#                     "slug":
#                         tour.slug,

#                     "adult_price":
#                         float(
#                             adult_price
#                         ),

#                     "image":
#                         request.build_absolute_uri(
#                             image.image.url
#                         )
#                         if image
#                         else None

#                 })

#             response_data.append({

#                 "id":
#                     category.id,

#                 "name":
#                     category.name,

#                 "tours":
#                     tours_data

#             })

#         return Response(
#             response_data
#         )
        
        
        
        
        
        


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