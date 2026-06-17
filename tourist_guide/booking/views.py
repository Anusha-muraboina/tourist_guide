from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.
def booking(request):
    return HttpResponse("Welcome to Tourist Guide")



# bookings/api_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from booking.serializers import (
    BookingCreateSerializer
)

class BookingCreateAPIView(APIView):

    def post(self, request):

        serializer = BookingCreateSerializer(
            data=request.data,
            context={
                "request": request
            }
        )

        if serializer.is_valid():

            booking = serializer.save()

            response_serializer = (
                BookingCreateSerializer(
                    booking,
                    context={
                        "request": request
                    }
                )
            )

            return Response({

                "success": True,

                "message":
                    "Booking created successfully",

                "coupon_applied":
                    booking.coupon_applied.code
                    if booking.coupon_applied
                    else None,

                # "sub_total":
                #     booking.sub_total,

                # "discount_amount":
                #     booking.discount_amount,

                # "total_amount":
                #     booking.total_amount,
                
                
                "sub_total":
                    str(
                        booking.sub_total
                    ),

                "discount_amount":
                    str(
                        booking.discount_amount
                    ),

                "total_amount":
                    str(
                        booking.total_amount
                    ),

                "data":
                    response_serializer.data

            }, status=status.HTTP_201_CREATED)

        return Response({

            "success": False,

            "errors":
                serializer.errors

        }, status=status.HTTP_400_BAD_REQUEST)
        


from django.shortcuts import render, get_object_or_404
from booking.models import Booking

def booking_success(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    return render(
        request,
        "booking_success.html",
        {
            "booking": booking
        }
    )
    
    
    
    
# booking/api_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from booking.models import Booking
from booking.serializers import BookingCreateSerializer


# class BookingUpdateAPIView(APIView):

#     def patch(self, request, booking_id):

#         try:

#             booking = Booking.objects.get(
#                 id=booking_id
#             )

#         except Booking.DoesNotExist:

#             return Response(
#                 {
#                     "success": False,
#                     "message": "Booking not found"
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         serializer = BookingCreateSerializer(
#             booking,
#             data=request.data,
#             partial=True,
#             context={
#                 "request": request
#             }
#         )
#         # serializer = BookingCreateSerializer(

#         #     booking,

#         #     data=request.data,

#         #     partial=True

#         # )
        

#         if serializer.is_valid():

#             serializer.save()
            
            
#             updated_booking = serializer.save()

#             updated_booking.refresh_from_db()

#             return Response({

#                 "success": True,

#                 "message": "Booking updated successfully",

#                 "sub_total": str(
#                     updated_booking.sub_total
#                 ),

#                 "discount_amount": str(
#                     updated_booking.discount_amount
#                 ),

#                 "total_amount": str(
#                     updated_booking.total_amount
#                 ),

#                 "coupon_applied":
#                     updated_booking.coupon_applied.code
#                     if updated_booking.coupon_applied
#                     else None,

#                 "data": serializer.data

#             })

#             # return Response({

#             #     "success": True,

#             #     "message":
#             #         "Booking updated successfully",
#             #         "sub_total":
#             #     str(
#             #             booking.sub_total
#             #         ),

#             #     "discount_amount":
#             #         str(
#             #             booking.discount_amount
#             #         ),

#             #     "total_amount":
#             #         str(
#             #             booking.total_amount
#             #         ),

#             #     "data":
#             #         serializer.data

#             # })

#         return Response({

#             "success": False,

#             "errors":
#                 serializer.errors

#         }, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
class BookingUpdateAPIView(APIView):

    def patch(self, request, booking_id):

        try:
            booking = Booking.objects.get(
                id=booking_id
            )

        except Booking.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Booking not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BookingCreateSerializer(
            booking,
            data=request.data,
            partial=True,
            context={
                "request": request
            }
        )

        if serializer.is_valid():

            updated_booking = serializer.save()

            updated_booking.refresh_from_db()

            print(
                "UPDATED SUBTOTAL =",
                updated_booking.sub_total
            )

            print(
                "UPDATED DISCOUNT =",
                updated_booking.discount_amount
            )

            print(
                "UPDATED TOTAL =",
                updated_booking.total_amount
            )

            return Response({

                "success": True,

                "message":
                    "Booking updated successfully",

                "sub_total":
                    str(
                        updated_booking.sub_total
                    ),

                "discount_amount":
                    str(
                        updated_booking.discount_amount
                    ),

                "total_amount":
                    str(
                        updated_booking.total_amount
                    ),

                "coupon_applied":
                    updated_booking.coupon_applied.code
                    if updated_booking.coupon_applied
                    else None,

                "data":
                    serializer.data

            })

        return Response({

            "success": False,

            "errors":
                serializer.errors

        }, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
from django.utils import timezone
from tourist.models import Tour
from coupon.models import Coupon
from decimal import Decimal       
class ApplyCouponAPIView(APIView):

    def post(self, request):

        coupon_code = request.data.get(
            "coupon_code"
        )

        tour_id = request.data.get(
            "tour"
        )

        adults = int(
            request.data.get(
                "adults",
                0
            )
        )

        children = int(
            request.data.get(
                "children",
                0
            )
        )

        infants = int(
            request.data.get(
                "infants",
                0
            )
        )

        try:

            tour = Tour.objects.get(
                id=tour_id
            )

        except Tour.DoesNotExist:

            return Response({

                "success": False,

                "message":
                    "Tour not found"

            })

        adult_price = Decimal("0")
        child_price = Decimal("0")
        infant_price = Decimal("0")

        adult_obj = tour.pricing.filter(
            person_type="adult"
        ).first()

        child_obj = tour.pricing.filter(
            person_type="child"
        ).first()

        infant_obj = tour.pricing.filter(
            person_type="infant"
        ).first()

        if adult_obj:
            adult_price = adult_obj.price

        if child_obj:
            child_price = child_obj.price

        if infant_obj:
            infant_price = infant_obj.price

        sub_total = (

            Decimal(adults) * adult_price +

            Decimal(children) * child_price +

            Decimal(infants) * infant_price

        )

        coupon = Coupon.objects.filter(

            code__iexact=
            coupon_code.strip()

        ).first()

        if not coupon:

            return Response({

                "success": False,

                "message":
                    "Invalid coupon code"

            })

        print("========== COUPON DEBUG ==========")
        print("Code:", coupon.code)
        print("Active:", coupon.is_active)
        print("Today:", timezone.now().date())
        print("Start:", coupon.start_date)
        print("End:", coupon.end_date)
        print("Usage Limit:", coupon.usage_limit)
        print("Used Count:", coupon.used_count)
        print("Valid:", coupon.is_valid())
        print("==================================")

        if not coupon.is_valid():

            return Response({

                "success": False,

                "message":
                    "Coupon expired or inactive"

            })

        # discount_amount = (
        #     coupon.calculate_discount(
        #         sub_total
        #     )
        # )
        
        
        print("SUB TOTAL =", sub_total)
        print("DISCOUNT TYPE =", coupon.discount_type)
        print("DISCOUNT VALUE =", coupon.discount_value)

        discount_amount = coupon.calculate_discount(sub_total)

        print("DISCOUNT AMOUNT =", discount_amount)

        total_amount = (
            sub_total -
            discount_amount
        )

        return Response({

            "success": True,

            "coupon":
                coupon.code,

            "sub_total":
                str(sub_total),

            "discount_amount":
                str(discount_amount),

            "total_amount":
                str(total_amount)

        })