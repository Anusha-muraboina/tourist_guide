from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import ContactUs

from django.http import HttpResponse
# def contact(request):
#     return HttpResponse("Welcome to Tourist Guide")


import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactUsSerializer
from django.conf import settings


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests

from .models import ContactUs
from .serializers import ContactUsSerializer   # make sure this exists


class ContactUsAPIView(APIView):

    def post(self, request, *args, **kwargs):

        # 1. Get reCAPTCHA token
        recaptcha_token = request.data.get("recaptcha_token")

        if not recaptcha_token:
            return Response(
                {
                    "success": False,
                    "message": "Please complete the reCAPTCHA."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Verify reCAPTCHA with Google
        try:
            recaptcha_response = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={
                    "secret": settings.RECAPTCHA_SECRET_KEY,
                    "response": recaptcha_token,
                    "remoteip": request.META.get("REMOTE_ADDR"),
                },
                timeout=10,
            )
            recaptcha_result = recaptcha_response.json()

        except requests.RequestException:
            return Response(
                {
                    "success": False,
                    "message": "Unable to verify reCAPTCHA. Please try again."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # 3. Check Google's response
        if not recaptcha_result.get("success"):
            return Response(
                {
                    "success": False,
                    "message": "reCAPTCHA verification failed. Please try again."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4. Get form data
        name = request.data.get("name", "").strip()
        email = request.data.get("email", "").strip()
        phone_number = request.data.get("phone_number", "").strip()
        message = request.data.get("message", "").strip()

        # 5. Validate required fields
        if not name:
            return Response(
                {"success": False, "message": "Name is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not email:
            return Response(
                {"success": False, "message": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not message:
            return Response(
                {"success": False, "message": "Message is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 6. Save to database using Serializer (Recommended)
        serializer = ContactUsSerializer(data={
            "name": name,
            "email": email,
            "phone_number": phone_number or None,
            "message": message,
        })

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Message sent successfully!"
                },
                status=status.HTTP_201_CREATED
            )

        # If serializer has errors
        return Response(
            {
                "success": False,
                "message": "Invalid data.",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

# class ContactUsAPIView(APIView):

#     def post(self, request, *args, **kwargs):

#         # -----------------------------
#         # 1. Get reCAPTCHA token
#         # -----------------------------
#         recaptcha_token = request.data.get("recaptcha_token")

#         if not recaptcha_token:
#             return Response(
#                 {
#                     "success": False,
#                     "message": "Please complete the reCAPTCHA."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # -----------------------------
#         # 2. Verify reCAPTCHA with Google
#         # -----------------------------
#         try:
#             recaptcha_response = requests.post(
#                 "https://www.google.com/recaptcha/api/siteverify",
#                 data={
#                     "secret": settings.RECAPTCHA_SECRET_KEY,
#                     "response": recaptcha_token,
#                     "remoteip": request.META.get("REMOTE_ADDR"),
#                 },
#                 timeout=10,
#             )

#             recaptcha_result = recaptcha_response.json()

#         except requests.RequestException:
#             return Response(
#                 {
#                     "success": False,
#                     "message": "Unable to verify reCAPTCHA. Please try again."
#                 },
#                 status=status.HTTP_503_SERVICE_UNAVAILABLE
#             )

#         # -----------------------------
#         # 3. Check Google's response
#         # -----------------------------
#         if not recaptcha_result.get("success"):
#             return Response(
#                 {
#                     "success": False,
#                     "message": "reCAPTCHA verification failed. Please try again."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # -----------------------------
#         # 4. Get contact form data
#         # -----------------------------
#         name = request.data.get("name", "").strip()
#         email = request.data.get("email", "").strip()
#         phone_number = request.data.get("phone_number", "").strip()
#         message = request.data.get("message", "").strip()

#         # -----------------------------
#         # 5. Validate fields
#         # -----------------------------
#         if not name:
#             return Response(
#                 {
#                     "success": False,
#                     "message": "Name is required."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         if not email:
#             return Response(
#                 {
#                     "success": False,
#                     "message": "Email is required."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         if not message:
#             return Response(
#                 {
#                     "success": False,
#                     "message": "Message is required."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # -----------------------------
#         # 6. Save your contact message
#         # -----------------------------

#         # Use your existing serializer/model here.
#         # Example:
#         #
#         # serializer = ContactSerializer(data={
#         #     "name": name,
#         #     "email": email,
#         #     "phone_number": phone_number,
#         #     "message": message,
#         # })
#         #
#         # if serializer.is_valid():
#         #     serializer.save()

#         return Response(
#             {
#                 "success": True,
#                 "message": "Message sent successfully!"
#             },
#             status=status.HTTP_200_OK
#         )
        
        
        
# # class ContactUsAPIView(APIView):

# #     # permission_classes = []

# #     def post(self, request):

# #         serializer = ContactUsSerializer(
# #             data=request.data
# #         )

# #         if serializer.is_valid():

# #             serializer.save()

# #             return Response(
# #                 {
# #                     "success": True,
# #                     "message": "Your message has been sent successfully."
# #                 },
# #                 status=status.HTTP_201_CREATED
# #             )

# #         return Response(
# #             {
# #                 "success": False,
# #                 "errors": serializer.errors
# #             },
# #             status=status.HTTP_400_BAD_REQUEST
# #         )
        
        


from django.shortcuts import render
# def contact(request):
#     return render(
#         request,
#         "pages/contact_us.html"
#     )
    
    

def contact(request):
    return render(
        request,
        "pages/contact_us.html",
        {
            "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
        }
    )