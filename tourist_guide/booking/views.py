from django.shortcuts import render
import razorpay
import json
from django.conf import settings
# Create your views here.
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from booking.models import CancelReason ,Invoice
# Create your views here.
def booking(request):
    return HttpResponse("Welcome to Tourist Guide")

razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)



# booking/razorpay_views.py

import razorpay
import json
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from booking.serializers import BookingCreateSerializer
from booking.models import Booking

razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


class CreateRazorpayOrderAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        amount = request.data.get("amount")  # in rupees

        if not amount:
            return Response({"success": False, "message": "Amount required"}, status=400)

        try:
            amount_paise = int(float(amount) * 100)

            order = razorpay_client.order.create({
                "amount": amount_paise,
                "currency": "INR",
                "payment_capture": 1
            })

            return Response({
                "success": True,
                "order_id": order["id"],
                "amount": order["amount"],
                "currency": order["currency"],
                "key": settings.RAZORPAY_KEY_ID
            })

        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=400)

class VerifyAndCreateBookingAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        # ========== 1. Verify Signature ==========
        try:
            razorpay_client.utility.verify_payment_signature({
                "razorpay_order_id": data.get("razorpay_order_id"),
                "razorpay_payment_id": data.get("razorpay_payment_id"),
                "razorpay_signature": data.get("razorpay_signature")
            })
        except Exception:
            return Response({
                "success": False,
                "message": "Payment verification failed"
            }, status=400)

        # ========== 2. Prepare Booking Data ==========
        booking_data = {
            "tour": data.get("tour"),
            "pricing": data.get("pricing"),                 # ← required
            "group_members": data.get("group_members", 1),
            # "adults": data.get("adults"),
            # "children": data.get("children"),
            # "infants": data.get("infants"),
            "tour_date": data.get("tour_date"),
            "tour_time": data.get("tour_time"),
            "guest_name": data.get("guest_name"),
            "guest_email": data.get("guest_email"),
            "guest_phone": data.get("guest_phone"),
            "payment_method": data.get("payment_method"),
            "guide": data.get("guide"),
            "coupon_code": data.get("coupon_code", ""),
        }

        serializer = BookingCreateSerializer(
            data=booking_data,
            context={"request": request}
        )

        if not serializer.is_valid():
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=400)

        # ========== 3. Create Booking ==========
        booking = serializer.save()
        
        booking.payment_id = data.get(
            "razorpay_payment_id"
        )

        booking.transaction_id = data.get(
            "razorpay_order_id"
        )

        booking.razorpay_order_id = data.get(
            "razorpay_order_id"
        )

        booking.razorpay_signature = data.get(
            "razorpay_signature"
        )

        # ========== 4. Save Razorpay IDs ==========
        booking.payment_id = data.get("razorpay_payment_id")
        booking.transaction_id = data.get("razorpay_order_id")   # or payment_id
        booking.razorpay_order_id = data.get("razorpay_order_id")
        booking.razorpay_signature = data.get("razorpay_signature")

        # Update payment status based on method
        if booking.payment_method == "partial_payment":
            booking.payment_status = "partial"
        elif booking.payment_method == "full_payment":
            booking.payment_status = "paid"
        else:
            booking.payment_status = "pending"

        # booking.status = "confirmed"
        booking.status = "pending"

        booking.guide_status = "pending"

        booking.guide_attempt = 1
        booking.save()

        return Response({
            "success": True,
            "message": "Payment successful & Booking created",
            "data": {
                "id": booking.id,
                "booking_id": booking.booking_id,
                "payment_id": booking.payment_id,
                "transaction_id": booking.transaction_id,
                "payment_status": booking.payment_status,
                "total_amount": str(booking.total_amount),
                "advance_amount": str(booking.advance_amount),
                "remaining_amount": str(booking.remaining_amount),
            }
        }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class RazorpayWebhookAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            webhook_body = request.body.decode("utf-8")
            webhook_signature = request.headers.get("X-Razorpay-Signature")

            razorpay_client.utility.verify_webhook_signature(
                webhook_body,
                webhook_signature,
                settings.RAZORPAY_WEBHOOK_SECRET
            )

            payload = json.loads(webhook_body)
            event = payload.get("event")

            if event == "payment.captured":
                payment = payload["payload"]["payment"]["entity"]
                payment_id = payment["id"]
                order_id = payment["order_id"]

                # Optional: update booking if needed
                Booking.objects.filter(
                    razorpay_order_id=order_id
                ).update(payment_status="paid")

            return Response({"status": "ok"})

        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=400)

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

       
# class ApplyCouponAPIView(APIView):

#     def post(self, request):

#         coupon_code = request.data.get(
#             "coupon_code"
#         )

#         tour_id = request.data.get(
#             "tour"
#         )

#         adults = int(
#             request.data.get(
#                 "adults",
#                 0
#             )
#         )

#         children = int(
#             request.data.get(
#                 "children",
#                 0
#             )
#         )

#         infants = int(
#             request.data.get(
#                 "infants",
#                 0
#             )
#         )

#         try:

#             tour = Tour.objects.get(
#                 id=tour_id
#             )

#         except Tour.DoesNotExist:

#             return Response({

#                 "success": False,

#                 "message":
#                     "Tour not found"

#             })

#         adult_price = Decimal("0")
#         child_price = Decimal("0")
#         infant_price = Decimal("0")
        
#         adult_obj = tour.pricing.filter(
#             person_type="adult"
#         ).first()

#         child_obj = tour.pricing.filter(
#             person_type="child"
#         ).first()

#         infant_obj = tour.pricing.filter(
#             person_type="infant"
#         ).first()

#         if adult_obj:
#             adult_price = adult_obj.price

#         if child_obj:
#             child_price = child_obj.price

#         if infant_obj:
#             infant_price = infant_obj.price

#         sub_total = (

#             Decimal(adults) * adult_price +

#             Decimal(children) * child_price +

#             Decimal(infants) * infant_price

#         )

#         coupon = Coupon.objects.filter(

#             code__iexact=
#             coupon_code.strip()

#         ).first()

#         if not coupon:

#             return Response({

#                 "success": False,

#                 "message":
#                     "Invalid coupon code"

#             })

#         print("========== COUPON DEBUG ==========")
#         print("Code:", coupon.code)
#         print("Active:", coupon.is_active)
#         print("Today:", timezone.now().date())
#         print("Start:", coupon.start_date)
#         print("End:", coupon.end_date)
#         print("Usage Limit:", coupon.usage_limit)
#         print("Used Count:", coupon.used_count)
#         print("Valid:", coupon.is_valid())
#         print("==================================")

#         if not coupon.is_valid():

#             return Response({

#                 "success": False,

#                 "message":
#                     "Coupon expired or inactive"

#             })

#         # discount_amount = (
#         #     coupon.calculate_discount(
#         #         sub_total
#         #     )
#         # )
        
        
#         print("SUB TOTAL =", sub_total)
#         print("DISCOUNT TYPE =", coupon.discount_type)
#         print("DISCOUNT VALUE =", coupon.discount_value)

#         discount_amount = coupon.calculate_discount(sub_total)

#         print("DISCOUNT AMOUNT =", discount_amount)

#         total_amount = (
#             sub_total -
#             discount_amount
#         )

#         return Response({

#             "success": True,

#             "coupon":
#                 coupon.code,

#             "sub_total":
#                 str(sub_total),

#             "discount_amount":
#                 str(discount_amount),

#             "total_amount":
#                 str(total_amount)

#         })
        
        
        


class ApplyCouponAPIView(APIView):

    def post(self, request):
        coupon_code = request.data.get("coupon_code")
        tour_id = request.data.get("tour")
        pricing_id = request.data.get("pricing")          # ← new

        try:
            tour = Tour.objects.get(id=tour_id)
        except Tour.DoesNotExist:
            return Response({
                "success": False,
                "message": "Tour not found"
            })

        # ---------- Get price from selected group ----------
        try:
            pricing = TourPricing.objects.get(
                id=pricing_id,
                tour=tour,
                is_active=True
            )
            sub_total = Decimal(str(pricing.group_price))
        except TourPricing.DoesNotExist:
            return Response({
                "success": False,
                "message": "Invalid pricing selected"
            })

        # ---------- Coupon ----------
        coupon = Coupon.objects.filter(
            code__iexact=coupon_code.strip()
        ).first()

        if not coupon:
            return Response({
                "success": False,
                "message": "Invalid coupon code"
            })

        if not coupon.is_valid():
            return Response({
                "success": False,
                "message": "Coupon expired or inactive"
            })

        discount_amount = coupon.calculate_discount(sub_total)
        total_amount = sub_total - discount_amount

        return Response({
            "success": True,
            "coupon": coupon.code,
            "sub_total": str(sub_total),
            "discount_amount": str(discount_amount),
            "total_amount": str(total_amount)
        })
        
        
        
from rest_framework.permissions import IsAuthenticated, AllowAny
from booking.models import Booking
from booking.serializers import BookingCreateSerializer


# class BookingListAPIView(APIView):

#     permission_classes = [AllowAny]

#     def get(self, request):

#         bookings = (
#             Booking.objects
#             .filter(
#                 user=request.user
#             )
#             .select_related(
#                 "tour",
#                 "guide"
#             )
#             .order_by(
#                 "-created_at"
#             )
#         )

#         serializer = BookingCreateSerializer(
#             bookings,
#             many=True,
#             context={
#                 "request": request
#             }
#         )

#         return Response({

#             "success": True,

#             "count":
#                 bookings.count(),

#             "data":
#                 serializer.data

#         })



from rest_framework.views import APIView
from rest_framework.response import Response

from booking.models import Booking
from booking.serializers import (
    BookingCreateSerializer ,BookingListSerializer
)

# class BookingListAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         if request.user.role == "guide":
#             bookings = (
#                 Booking.objects
#                 .filter(guide=request.user)
#                 .select_related("tour", "guide")
#                 .order_by("-created_at")
#             )
#         else:
#             bookings = (
#                 Booking.objects
#                 .filter(user=request.user)
#                 .select_related("tour", "guide")
#                 .order_by("-created_at")
#             )

#         serializer = BookingListSerializer(
#             bookings,
#             many=True,
#             context={"request": request}
#         )

#         return Response({
#             "data": serializer.data
#         })



from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from .models import Booking
from .serializers import BookingListSerializer


# ============================================================
# BOOKING LIST API
# ============================================================

class BookingListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role == "guide":
            bookings = (
                Booking.objects
                .filter(guide=request.user)
                .select_related("tour", "guide")
                .order_by("-created_at")
            )
        else:
            bookings = (
                Booking.objects
                .filter(user=request.user)
                .select_related("tour", "guide")
                .order_by("-created_at")
            )

        serializer = BookingListSerializer(
            bookings,
            many=True,
            context={"request": request}
        )

        return Response({
            "data": serializer.data
        })


# ============================================================
# GUIDE VERIFY BOOKING CODE
# confirmed → on_process
# ============================================================

class VerifyBookingCodeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):

        # Only guide can verify
        if request.user.role != "guide":
            return Response(
                {
                    "success": False,
                    "message": "Only guides can verify bookings."
                },
                status=403
            )

        # Get only this guide's booking
        try:
            booking = Booking.objects.get(
                id=booking_id,
                guide=request.user
            )
        except Booking.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Booking not found."
                },
                status=404
            )

        # Verification is allowed ONLY for confirmed booking
        if booking.status != "confirmed":
            return Response(
                {
                    "success": False,
                    "message": "This booking cannot be verified now."
                },
                status=400
            )

        # Get entered code
        code = str(
            request.data.get("code", "")
        ).strip()

        if not code:
            return Response(
                {
                    "success": False,
                    "message": "Verification code is required."
                },
                status=400
            )

        # Check verification code
        if code != str(booking.verification_code):
            return Response(
                {
                    "success": False,
                    "message": "Invalid verification code."
                },
                status=400
            )

        # Correct code → ON PROCESS
        booking.status = "on_process"

        # Optional timestamp if your model has verified_at
        if hasattr(booking, "verified_at"):
            booking.verified_at = timezone.now()

            booking.save(
                update_fields=[
                    "status",
                    "verified_at"
                ]
            )
        else:
            booking.save(
                update_fields=["status"]
            )

        return Response({
            "success": True,
            "message": "Booking verified successfully. Tour is now on process.",
            "status": booking.status
        })


# ============================================================
# GUIDE COMPLETE BOOKING
# on_process → completed
# ============================================================

# class CompleteBookingAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, booking_id):

#         # Only guide can complete
#         if request.user.role != "guide":
#             return Response(
#                 {
#                     "success": False,
#                     "message": "Only guides can complete bookings."
#                 },
#                 status=403
#             )

#         # Get only this guide's booking
#         try:
#             booking = Booking.objects.get(
#                 id=booking_id,
#                 guide=request.user
#             )
#         except Booking.DoesNotExist:
#             return Response(
#                 {
#                     "success": False,
#                     "message": "Booking not found."
#                 },
#                 status=404
#             )

#         # Complete ONLY on-process booking
#         if booking.status != "on_process":
#             return Response(
#                 {
#                     "success": False,
#                     "message": "Only an on-process booking can be completed."
#                 },
#                 status=400
#             )

#         # ON PROCESS → COMPLETED
#         booking.status = "completed"
#         booking.payment_status ="paid"

#         # Optional timestamp if your model has completed_at
#         if hasattr(booking, "completed_at"):
#             booking.completed_at = timezone.now()
            

#             booking.save(
#                 update_fields=[
#                     "status",
#                     "completed_at"
#                 ]
#             )
            
#         else:
#             booking.save(
                
#                 update_fields=["status"]
#             )

#         return Response({
#             "success": True,
#             "message": "Booking completed successfully.",
#             "status": booking.status
#         })
        
        
        
class CompleteBookingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):

        # ==========================================
        # ONLY GUIDE CAN COMPLETE
        # ==========================================
        if getattr(request.user, "role", None) != "guide":
            return Response(
                {
                    "success": False,
                    "message": "Only guides can complete bookings."
                },
                status=403
            )

        # ==========================================
        # GET THIS GUIDE'S BOOKING
        # ==========================================
        try:
            booking = Booking.objects.get(
                id=booking_id,
                guide=request.user
            )
        except Booking.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Booking not found."
                },
                status=404
            )

        # ==========================================
        # ONLY ON_PROCESS CAN BE COMPLETED
        # ==========================================
        if booking.status != "on_process":
            return Response(
                {
                    "success": False,
                    "message": "Only an on-process booking can be completed."
                },
                status=400
            )

        # ==========================================
        # ON_PROCESS → COMPLETED
        # ==========================================
        booking.status = "completed"

        # Payment becomes fully paid
        booking.payment_status = "paid"

        # ==========================================
        # OPTIONAL COMPLETION TIMESTAMP
        # ==========================================
        update_fields = [
            "status",
            "payment_status",
        ]

        if hasattr(booking, "completed_at"):
            booking.completed_at = timezone.now()
            update_fields.append("completed_at")

        # ==========================================
        # SAVE
        # ==========================================
        booking.save(
            update_fields=update_fields
        )

        # ==========================================
        # RESPONSE
        # ==========================================
        return Response(
            {
                "success": True,
                "message": "Booking completed successfully.",
                "status": booking.status,
                "payment_status": booking.payment_status
            },
            status=200
        )
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction

from .models import Booking

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import random

from .models import Booking


@login_required
@require_POST
def guide_accept_booking(request, booking_id):

    # ============================================================
    # ONLY GUIDE CAN ACCEPT
    # ============================================================

    if getattr(request.user, "role", None) != "guide":
        return JsonResponse(
            {
                "success": False,
                "message": "Only guides can accept bookings."
            },
            status=403
        )

    # ============================================================
    # TRANSACTION
    # IMPORTANT:
    # select_for_update() MUST be inside atomic()
    # ============================================================

    try:

        with transaction.atomic():

            booking = (
                Booking.objects
                .select_for_update()
                .select_related(
                    "tour",
                    "user",
                    "guide"
                )
                .get(id=booking_id)
            )

            # ====================================================
            # SECURITY CHECK
            # Make sure this booking belongs to this guide
            # ====================================================

            if booking.guide_id != request.user.id:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "This booking is not assigned to you."
                    },
                    status=403
                )

            # ====================================================
            # BOOKING MUST BE PENDING
            # ====================================================

            if booking.status != "pending":
                return JsonResponse(
                    {
                        "success": False,
                        "message": "This booking is no longer pending."
                    },
                    status=400
                )

            # ====================================================
            # GUIDE MUST STILL BE PENDING
            # ====================================================

            if booking.guide_status != "pending":
                return JsonResponse(
                    {
                        "success": False,
                        "message": (
                            "You have already responded to this booking."
                        )
                    },
                    status=400
                )

            # ====================================================
            # GENERATE 6-DIGIT VERIFICATION CODE
            # ====================================================

            verification_code = str(
                random.randint(100000, 999999)
            )

            # ====================================================
            # ACCEPT BOOKING
            # ====================================================

            booking.verification_code = verification_code

            booking.guide_status = "accepted"

            booking.status = "confirmed"

            # ====================================================
            # SAVE
            # ====================================================

            booking.save(
                update_fields=[
                    "verification_code",
                    "guide_status",
                    "status"
                ]
            )

    except Booking.DoesNotExist:

        return JsonResponse(
            {
                "success": False,
                "message": "Booking not found."
            },
            status=404
        )

    # ============================================================
    # SEND CONFIRMATION EMAIL TO TOURIST
    # ============================================================

    email_sent = False

    try:

        subject = (
            f"Booking Confirmed - "
            f"{booking.booking_id}"
        )

        message = f"""
Hello {booking.guest_name},

Great news!

Your tour booking has been confirmed.

----------------------------------------
BOOKING DETAILS
----------------------------------------

Booking ID:
{booking.booking_id}

Tour:
{booking.tour.title if booking.tour else "Tour"}

Tour Date:
{booking.tour_date}

Tour Time:
{booking.tour_time}

Guide:
{booking.guide.username if booking.guide else "Assigned Guide"}

----------------------------------------
VERIFICATION CODE
----------------------------------------

Your 6-digit verification code is:

{booking.verification_code}

Please keep this code safe.

You will need to provide this code to
your guide when you are ready to start
your tour.

----------------------------------------

Thank you for booking with us.

Regards,
{getattr(settings, "SITE_NAME", "Tourist Guide")}
"""

        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[booking.guest_email],
        )

        email.send(
            fail_silently=False
        )

        email_sent = True

    except Exception as e:

        print(
            "Guide accepted email error:",
            e
        )

    # ============================================================
    # RESPONSE
    # ============================================================

    return JsonResponse(
        {
            "success": True,

            "message": (
                "Booking accepted successfully. "
                "Verification code has been generated "
                "and sent to the tourist."
            ),

            "booking_id": booking.booking_id,

            "booking_database_id": booking.id,

            "guide_id": booking.guide_id,

            "guide_status": booking.guide_status,

            "booking_status": booking.status,

            "verification_code_generated": True,

            "email_sent": email_sent,
        }
        
    )
  
  
  
  
  
  
  
@login_required
@require_POST
def guide_decline_booking(request, booking_id):

    if getattr(request.user, "role", None) != "guide":
        return JsonResponse(
            {
                "success": False,
                "message": "Only guides can decline bookings."
            },
            status=403
        )

    try:

        with transaction.atomic():

            booking = (
                Booking.objects
                .select_for_update()
                .select_related(
                    "tour",
                    "user",
                    "guide"
                )
                .get(id=booking_id)
            )

            # SECURITY CHECK

            if booking.guide_id != request.user.id:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "This booking is not assigned to you."
                    },
                    status=403
                )

            # BOOKING MUST BE PENDING

            if booking.status != "pending":
                return JsonResponse(
                    {
                        "success": False,
                        "message": "This booking is no longer pending."
                    },
                    status=400
                )

            # GUIDE MUST BE PENDING

            if booking.guide_status != "pending":
                return JsonResponse(
                    {
                        "success": False,
                        "message": (
                            "You have already responded to this booking."
                        )
                    },
                    status=400
                )

            # ====================================================
            # SAVE DECLINED GUIDE
            # ====================================================

            declined_ids = list(
                booking.declined_guides or []
            )

            if request.user.id not in declined_ids:
                declined_ids.append(
                    request.user.id
                )

            booking.declined_guides = declined_ids

            booking.guide_status = "declined"

            booking.status = "pending"

            booking.save(
                update_fields=[
                    "declined_guides",
                    "guide_status",
                    "status"
                ]
            )

            # ====================================================
            # FIND NEXT GUIDE
            # ====================================================

            next_guide = booking.get_next_guide()

            if next_guide:

                booking.guide = next_guide

                booking.guide_status = "pending"

                booking.guide_attempt += 1

                booking.status = "pending"

                booking.save(
                    update_fields=[
                        "guide",
                        "guide_status",
                        "guide_attempt",
                        "status"
                    ]
                )

                next_guide_id = next_guide.id

                next_guide_name = (
                    getattr(
                        next_guide,
                        "username",
                        None
                    )
                    or getattr(
                        next_guide,
                        "email",
                        None
                    )
                    or str(next_guide.id)
                )

            else:

                next_guide_id = None
                next_guide_name = None

    except Booking.DoesNotExist:

        return JsonResponse(
            {
                "success": False,
                "message": "Booking not found."
            },
            status=404
        )

    # ============================================================
    # ADMIN EMAIL
    # ============================================================

    try:

        subject = (
            f"Guide Declined Booking - "
            f"{booking.booking_id}"
        )

        message = f"""
Booking ID: {booking.booking_id}

Tour:
{booking.tour.title if booking.tour else "Tour"}

Declined Guide:
{getattr(request.user, "username", request.user.email)}

Guide ID:
{request.user.id}

Booking Status:
{booking.status}

Guide Status:
declined

Next Guide:
{next_guide_name or "No available guide"}

The booking remains pending.
"""

        admin_email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMIN_EMAIL],
        )

        admin_email.send(
            fail_silently=False
        )

    except Exception as e:

        print(
            "Guide decline admin email error:",
            e
        )

    # ============================================================
    # RESPONSE
    # ============================================================

    if next_guide_id:

        return JsonResponse(
            {
                "success": True,
                "message": (
                    "Booking declined. "
                    "The booking has been sent "
                    "to the next guide."
                ),
                "booking_id": booking.booking_id,
                "guide_status": "pending",
                "booking_status": "pending",
                "next_guide_id": next_guide_id,
                "next_guide_name": next_guide_name,
            }
        )

    return JsonResponse(
        {
            "success": True,
            "message": (
                "Booking declined. "
                "No other guide is currently available. "
                "Booking remains pending."
            ),
            "booking_id": booking.booking_id,
            "guide_status": "declined",
            "booking_status": "pending",
            "next_guide_id": None,
            "next_guide_name": None,
        }
    )
    
    
    
    
@login_required
def guide_pending_bookings(request):

    if getattr(request.user, "role", None) != "guide":
        return JsonResponse(
            {
                "success": False,
                "message": "Only guides can view guide bookings."
            },
            status=403
        )

    # ==========================================
    # ALL BOOKINGS ASSIGNED TO THIS GUIDE
    # ==========================================
    bookings = (
        Booking.objects
        .filter(guide=request.user)
        .select_related("tour", "user", "guide")
        .order_by("-id")
    )

    data = []

    for booking in bookings:

        # --------------------------------------
        # TOUR NAME
        # --------------------------------------
        tour_name = ""

        if booking.tour:
            tour_name = getattr(
                booking.tour,
                "title",
                getattr(booking.tour, "name", "")
            )

        # --------------------------------------
        # DATE
        # --------------------------------------
        tour_date = getattr(
            booking,
            "tour_date",
            None
        )

        if tour_date:
            tour_date = str(tour_date)

        # --------------------------------------
        # TIME
        # --------------------------------------
        tour_time = getattr(
            booking,
            "tour_time",
            None
        )

        if tour_time:
            tour_time = str(tour_time)

        # --------------------------------------
        # GUIDE PROFILE
        # --------------------------------------
        selected_guide = None

        if booking.guide:

            profile_image = ""

            try:
                if booking.guide.profile_image:
                    profile_image = booking.guide.profile_image.url
            except (ValueError, AttributeError):
                profile_image = ""

            selected_guide = {
                "id": booking.guide.id,

                "username": str(
                    booking.guide.username or ""
                ),

                "email": str(
                    getattr(
                        booking.guide,
                        "email",
                        ""
                    ) or ""
                ),

                "phone_number": str(
                    getattr(
                        booking.guide,
                        "phone_number",
                        ""
                    ) or ""
                ),

                "profile_image": profile_image,

                "location": str(
                    getattr(
                        booking.guide,
                        "location",
                        ""
                    ) or ""
                ),

                "state": str(
                    getattr(
                        booking.guide,
                        "state",
                        ""
                    ) or ""
                ),
            }

        # --------------------------------------
        # BOOKING
        # --------------------------------------
        data.append({

            "id": booking.id,

            "booking_id": booking.booking_id,

            # ALL STATUS VALUES
            "status": booking.status,

            "booking_status": booking.status,

            # GUIDE STATUS
            "guide_id": booking.guide_id,

            "guide_status": booking.guide_status,

            "guide_attempt": booking.guide_attempt,

            # TOUR
            "tour_name": tour_name,

            "tour_date": tour_date,

            "tour_time": tour_time,

            # GUEST
            "guest_name": str(
                booking.guest_name or ""
            ),

            "guest_email": str(
                booking.guest_email or ""
            ),

            "guest_phone": str(
                booking.guest_phone or ""
            ),

            # PAYMENT
            "total_amount": float(
                booking.total_amount or 0
            ),

            # GUIDE
            "selected_guide": selected_guide,
        })

    return JsonResponse({
        "success": True,
        "count": len(data),
        "data": data,
    })
    
# class BookingListAPIView(APIView):

#     def get(self, request):

#         bookings = (
#             Booking.objects
#             .select_related(
#                 "tour",
#                 "guide"
#             )
#             .order_by(
#                 "-created_at"
#             )
#         )

#         serializer = BookingListSerializer(
#             bookings,
#             many=True
#         )

#         return Response({

#             # "success": True,

#             # "count":
#             #     bookings.count(),

#             "data":
#                 serializer.data

#         })

# class BookingListAPIView(APIView):

#     def get(self, request):

#         bookings = (
#             Booking.objects
#             .select_related(
#                 "tour",
#                 "user",
#                 "guide"
#             )
#             .order_by(
#                 "-created_at"
#             )
#         )

#         serializer = (
#             BookingCreateSerializer(
#                 bookings,
#                 many=True,
#                 context={
#                     "request": request
#                 }
#             )
#         )

#         return Response({

#             # "success": True,

#             # "count":
#             #     bookings.count(),

#             "data":
#                 serializer.data

#         })



# class BookingDetailAPIView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(
#         self,
#         request,
#         booking_id
#     ):

#         try:

#             booking = (
#                 Booking.objects
#                 .select_related(
#                     "tour",
#                     "guide"
#                 )
#                 .get(
#                     id=booking_id,
#                     user=request.user
#                 )
#             )

#         except Booking.DoesNotExist:

#             return Response({

#                 "success": False,

#                 "message":
#                     "Booking not found"

#             }, status=404)

#         serializer = BookingCreateSerializer(

#             booking,

#             context={
#                 "request": request
#             }

#         )

#         return Response({

#             "success": True,

#             "data":
#                 serializer.data

#         })
        
from django.db.models import Q

class BookingDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):

        try:

            booking = (
                Booking.objects
                .select_related(
                    "tour",
                    "guide"
                )
                .get(
                    Q(user=request.user) |
                    Q(guide=request.user),
                    id=booking_id
                )
            )

        except Booking.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Booking not found"
                },
                status=404
            )

        serializer = BookingCreateSerializer(
            booking,
            context={
                "request": request
            }
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )  
        
        
        
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def my_bookings(request):

    return render(
        request,
        "my_bookings.html"
    )
    
    
    
    
from django.shortcuts import render, get_object_or_404
from booking.models import Booking, Invoice


def view_invoice(request, booking_id):

    booking = get_object_or_404(
        Booking.objects.select_related(
            "tour",
            "guide",
            "user"
        ),
        booking_id=booking_id
    )

    invoice, _ = Invoice.objects.get_or_create(
        booking=booking,
        # defaults={
        #     "user": booking.user
        # }
    )

    return render(
        request,
        "emails/invoice.html",
        {
            "invoice": invoice,
            "booking": booking
        }
    ) 

from booking.serializers import *

class CancelReasonListAPI(ListAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = CancelReason.objects.filter(is_active=True)
    serializer_class = CancelReasonSerializer
    
    
    
    
class CancelBookingAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):

        try:
            booking = Booking.objects.get(
                booking_id=booking_id,
                user=request.user
            )

        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking not found"},
                status=404
            )

        reason_id = request.data.get("reason")
        comment = request.data.get("comment", "")

        reason = None

        if reason_id:
            reason = CancelReason.objects.filter(
                id=reason_id
            ).first()

        try:

            booking.cancel_booking(
                user=request.user,
                reason=reason,
                comment=comment
            )

        except ValidationError as e:
            return Response(
                {"error": e.messages[0]},
                status=400
            )

        return Response({
            "message": "Booking cancelled successfully"
        })
        
        
@login_required
def cancel_booking_page(request, booking_id):

    booking = get_object_or_404(
        Booking,
        booking_id=booking_id,   # using booking code 👍
        user=request.user
    )

    return render(
        request,
        "cancelled_booking.html",
        {
            "booking": booking   # ⭐ PASS OBJECT, not just id
        }
    )
    
    
