from django.shortcuts import render
from rest_framework.parsers import (
    MultiPartParser,
    FormParser
)
# Create your views here.
from django.http import HttpResponse
# Create your views here.
def register(request):
    # return HttpResponse("Welcome to Tourist Guide")
    # render(request )
    return render(request, 'register.html')
    
def login_view(request):

    return render(request, 'login.html')
    
def forgot_password(request):

    return render(
        request,
        'forgot_password.html'
    )
    
def confirm_password(request):

    return render(
        request,
        'confirm_password.html'
    )
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import (
    render,
    redirect
)

from django.contrib import messages

from django.contrib.auth.hashers import make_password

from .models import User
from django.contrib.auth import login, logout

from .serializers import (
    RegisterSerializer,
    LoginSerializer
)
from django.shortcuts import render

from django.contrib.auth import (
    login as auth_login,
    logout,
    authenticate
)


from .models import Location
from .serializers import LocationSerializer



    
    
# class RegisterAPIView(APIView):
#     parser_classes = [
#         MultiPartParser,
#         FormParser
#     ]
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()

#             return Response(
#                 {
#                     'message': 'User registered successfully',
#                     'data': serializer.data
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )


import random
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, RegistrationOTP
from .serializers import RegisterSerializer


# class RegisterAPIView(APIView):

#     def post(self, request):

#         serializer = RegisterSerializer(data=request.data)

#         # Validate registration data
#         if not serializer.is_valid():
#             return Response(
#                 serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         email = serializer.validated_data["email"]

#         # Check if user already exists
#         if User.objects.filter(email=email).exists():
#             return Response(
#                 {
#                     "detail": "An account with this email already exists."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Generate 6-digit OTP
#         otp = str(random.randint(100000, 999999))

#         # OTP expires after 10 minutes
#         expires_at = timezone.now() + timedelta(minutes=10)

#         # Create or update OTP
#         RegistrationOTP.objects.update_or_create(
#             email=email,
#             defaults={
#                 "otp": otp,
#                 "expires_at": expires_at,
#             }
#         )

#         # Send OTP email
#         try:

#             send_mail(
#                 subject="Your Registration OTP",
#                 message=f"""
# Hello,

# Your OTP for registration is:

# {otp}

# This OTP is valid for 10 minutes.

# If you did not request this registration, please ignore this email.

# Regards,
# Tourist Guide Team
# """,
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=[email],
#                 fail_silently=False,
#             )

#         except Exception as e:

#             # Remove OTP if email sending fails
#             RegistrationOTP.objects.filter(email=email).delete()

#             return Response(
#                 {
#                     "detail": "Unable to send OTP email.",
#                     "error": str(e)
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#         return Response(
#             {
#                 "message": "OTP sent successfully.",
#                 "otp_required": True,
#                 "email": email,
#             },
#             status=status.HTTP_200_OK
#         )
        
        
        

class RegisterAPIView(APIView):

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data["email"]

        # =================================================
        # CHECK EXISTING USER
        # =================================================

        if User.objects.filter(
            email=email
        ).exists():

            return Response(
                {
                    "detail":
                        "An account with this email already exists."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # =================================================
        # GENERATE OTP
        # =================================================

        otp = str(
            random.randint(
                100000,
                999999
            )
        )

        expires_at = (
            timezone.now()
            + timedelta(minutes=10)
        )

        # =================================================
        # IMPORTANT:
        # update_or_create prevents duplicate email error
        # =================================================

        RegistrationOTP.objects.update_or_create(

            email=email,

            defaults={
                "otp": otp,
                "expires_at": expires_at,
            }
        )

        # =================================================
        # SEND EMAIL
        # =================================================

        try:

            send_mail(

                subject="Your Registration OTP",

                message=(
                    f"Your registration OTP is: {otp}\n\n"
                    f"This OTP is valid for 10 minutes."
                ),

                from_email=settings.DEFAULT_FROM_EMAIL,

                recipient_list=[
                    email
                ],

                fail_silently=False,
            )

        except Exception as e:

            RegistrationOTP.objects.filter(
                email=email
            ).delete()

            return Response(

                {
                    "detail":
                        "Unable to send OTP email.",

                    "error":
                        str(e),
                },

                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(

            {
                "message":
                    "OTP sent successfully.",

                "otp_required":
                    True,

                "email":
                    email,
            },

            status=status.HTTP_200_OK
        )



import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail

from .models import *
from django.conf import settings
class VerifyRegistrationOTPAPIView(APIView):

    def post(self, request):

        email = request.data.get("email")
        otp = request.data.get("otp")

        # -----------------------------------------
        # CHECK INPUT
        # -----------------------------------------

        if not email:

            return Response(
                {
                    "error": "Email is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not otp:

            return Response(
                {
                    "error": "OTP is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # FIND OTP
        # -----------------------------------------

        try:

            otp_record = RegistrationOTP.objects.get(
                email=email
            )

        except RegistrationOTP.DoesNotExist:

            return Response(
                {
                    "error": "OTP not found. Please request a new OTP."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # CHECK EXPIRY
        # -----------------------------------------

        if otp_record.is_expired():

            otp_record.delete()

            return Response(
                {
                    "error": "OTP has expired. Please request a new OTP."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # CHECK OTP
        # -----------------------------------------

        if str(otp_record.otp) != str(otp):

            return Response(
                {
                    "error": "Invalid OTP."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # CHECK USER AGAIN
        # -----------------------------------------

        if User.objects.filter(email=email).exists():

            otp_record.delete()

            return Response(
                {
                    "error": "An account with this email already exists."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # IMPORTANT
        #
        # We need the original registration data
        # to create the user.
        #
        # If you are using only this simple OTP model,
        # the frontend must send the registration
        # data again together with the OTP.
        # -----------------------------------------

        registration_data = request.data.copy()

        registration_data.pop("otp", None)

        # -----------------------------------------
        # CREATE USER
        # -----------------------------------------

        serializer = RegisterSerializer(
            data=registration_data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.save()
        
        auth_login(request, user)

        # -----------------------------------------
        # OTP SUCCESS
        # -----------------------------------------

        otp_record.delete()

        return Response(
            {
                "message": "Email verified successfully. Registration completed.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                    "is_verified": user.is_verified
                }
            },
            status=status.HTTP_201_CREATED
        )
        

class ResendRegistrationOTPAPIView(APIView):

    def post(self, request):

        email = request.data.get("email")

        if not email:

            return Response(
                {
                    "error": "Email is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # CHECK IF USER ALREADY EXISTS
        # -----------------------------------------

        if User.objects.filter(email=email).exists():

            return Response(
                {
                    "error": "An account with this email already exists."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # GENERATE NEW OTP
        # -----------------------------------------

        otp = str(
            random.randint(100000, 999999)
        )

        # -----------------------------------------
        # DELETE OLD OTP
        # -----------------------------------------

        RegistrationOTP.objects.filter(
            email=email
        ).delete()

        # -----------------------------------------
        # CREATE NEW OTP
        # -----------------------------------------

        otp_record = RegistrationOTP(
            email=email,
            otp=otp,
            expires_at=timezone.now() + timedelta(minutes=10)
        )

        otp_record.save()

        # -----------------------------------------
        # SEND EMAIL
        # -----------------------------------------

        subject = "Your New Email Verification OTP"

        message = f"""
Hello,

Your new email verification OTP is:

{otp}

This OTP is valid for 10 minutes.

Please do not share this OTP with anyone.

Regards,
Samanvaya Construction
"""

        try:

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False
            )

        except Exception as e:

            otp_record.delete()

            return Response(
                {
                    "error": "Unable to send OTP email.",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                "message": "New OTP sent successfully.",
                "email": email
            },
            status=status.HTTP_200_OK
        )

class LoginAPIView(APIView):

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.validated_data["user"]

            auth_login(request, user)

            return Response(
                {
                    "success": True,
                    "message": "Login successful",
                    "email": user.email,
                    "role": user.role,
                    "redirect_url": "/",
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
# from django.shortcuts import redirect
# from django.contrib.auth import logout

# from rest_framework.views import APIView


class LogoutAPIView(APIView):
    def post(self, request):

        logout(request)

        return Response(
            {
                'message': 'Logout successful',
                'redirect_url': '/'
            },
            status=status.HTTP_200_OK
        )
# =========================================
# FORGOT PASSWORD API
# =========================================
# =========================================
# FORGOT PASSWORD API
# =========================================

class ForgotPasswordAPIView(APIView):

    def post(self, request):

        step = request.data.get(
            'step'
        )



        # =====================================
        # STEP 1 → VERIFY EMAIL
        # =====================================

        if step == 'verify_email':

            email = request.data.get(
                'email'
            )

            try:

                User.objects.get(
                    email=email
                )

                request.session[
                    'reset_email'
                ] = email

                return Response(
                    {
                        'message': 'Email verified successfully',
                        'show_password_fields': True
                    },
                    status=status.HTTP_200_OK
                )

            except User.DoesNotExist:

                return Response(
                    {
                        'error': 'Email does not exist'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )



        # =====================================
        # STEP 2 → UPDATE PASSWORD
        # =====================================

        elif step == 'reset_password':

            email = request.session.get(
                'reset_email'
            )

            if not email:

                return Response(
                    {
                        'error': 'Session expired'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            password = request.data.get(
                'password'
            )

            confirm_password = request.data.get(
                'confirm_password'
            )



            # PASSWORD MATCH

            if password != confirm_password:

                return Response(
                    {
                        'error': 'Passwords do not match'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )




            # UPDATE PASSWORD

            user = User.objects.get(
                email=email
            )

            user.password = make_password(
                password
            )

            user.save()



            # CLEAR SESSION

            del request.session[
                'reset_email'
            ]



            return Response(
                {
                    'message': 'Password updated successfully'
                },
                status=status.HTTP_200_OK
            )



        return Response(
            {
                'error': 'Invalid step'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
        
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
ProfileSerializer,
ProfileUpdateSerializer
)


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    ProfileSerializer,
    ProfileUpdateSerializer,
)

from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
)
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    ProfileSerializer,
    ProfileUpdateSerializer,
)


# ============================================================
# PROFILE PAGE
# ============================================================

@login_required
@ensure_csrf_cookie
def profile_page(request):

    return render(
        request,
        "profile.html"
    )

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
)
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    ProfileSerializer,
    ProfileUpdateSerializer,
)


# ============================================================
# PROFILE PAGE
# ============================================================
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
)
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    ProfileSerializer,
    ProfileUpdateSerializer,
)


# ============================================================
# PROFILE PAGE
# ============================================================

@login_required
def profile_page(request):

    csrf_token = get_token(request)

    return render(
        request,
        "profile.html",
        {
            "csrf_token_value": csrf_token
        }
    )


# ============================================================
# PROFILE API
# ============================================================

class ProfileAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    parser_classes = [
        MultiPartParser,
        FormParser
    ]

    # ========================================================
    # GET
    # ========================================================

    def get(self, request):

        serializer = ProfileSerializer(
            request.user,
            context={
                "request": request
            }
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    # ========================================================
    # PUT
    # ========================================================

    def put(self, request):

        print("====================================")
        print("PROFILE UPDATE")
        print("USER:", request.user)
        print("DATA:", request.data)
        print("FILES:", request.FILES)
        print("====================================")

        serializer = ProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={
                "request": request
            }
        )

        if not serializer.is_valid():

            print(
                "PROFILE ERRORS:",
                serializer.errors
            )

            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        request.user.refresh_from_db()

        profile_serializer = ProfileSerializer(
            request.user,
            context={
                "request": request
            }
        )

        return Response(
            {
                "success": True,
                "message": "Profile updated successfully.",
                "data": profile_serializer.data
            },
            status=status.HTTP_200_OK
        )

# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required


# @login_required
# def profile_page(request):

#     return render(
#         request,
#         "profile.html"
#     )


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response

from .models import Location
from .serializers import LocationSerializer




from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Location


class LocationListAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        locations = Location.objects.filter(
            is_active=True
        ).order_by(
            "state",
            "district",
            "city"
        )

        serializer = LocationSerializer(
            locations,
            many=True
        )

        return Response(serializer.data)
# class LocationListAPIView(APIView):

#     permission_classes = [AllowAny]

#     def get(
#         self,
#         request
#     ):

#         # Only guides should use this API

#         if request.user.role != "guide":

#             return Response([])


#         locations = Location.objects.filter(
#             is_active=True
#         )


#         serializer = LocationSerializer(
#             locations,
#             many=True
#         )


#         return Response(
#             serializer.data
#         )
        
        
        
        
        
        
        
        
        
        
        
from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count

from .models import User
from rating.models import Rating


def guide_detail(request, guide_id):
    """
    Public guide profile page.

    Phone number and email are intentionally NOT sent
    to the template.
    """

    guide = get_object_or_404(
        User.objects
        .select_related("guide_profile")
        .prefetch_related("locations"),
        id=guide_id,
        role="guide",
        is_active=True,
    )

    # Only active reviews belonging to this guide
    ratings = (
        Rating.objects
        .filter(
            guide=guide,
            active=True,
        )
        .select_related("user", "tour")
        .prefetch_related("images")
        .order_by("-created_at")
    )

    rating_summary = ratings.aggregate(
        average_rating=Avg("rating"),
        total_reviews=Count("id"),
    )

    average_rating = rating_summary["average_rating"] or 0
    total_reviews = rating_summary["total_reviews"] or 0

    # Rating distribution
    rating_distribution = {}

    for star in range(5, 0, -1):
        count = ratings.filter(
            rating__gte=star,
            rating__lt=star + 1,
        ).count()

        percentage = (
            round((count / total_reviews) * 100)
            if total_reviews
            else 0
        )

        rating_distribution[star] = {
            "count": count,
            "percentage": percentage,
        }

    context = {
        "guide": guide,
        "ratings": ratings,
        "average_rating": average_rating,
        "total_reviews": total_reviews,
        "rating_distribution": rating_distribution,
    }

    return render(
        request,
        "guide_detail.html",
        context,
    )