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


class LocationListAPIView(APIView):

    # permission_classes = [
    #     IsAuthenticated
    # ]

    def get(self, request):

        locations = Location.objects.filter(
            is_active=True
        )

        serializer = LocationSerializer(
            locations,
            many=True
        )

        return Response(serializer.data)
    
    
class RegisterAPIView(APIView):
    parser_classes = [
        MultiPartParser,
        FormParser
    ]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    'message': 'User registered successfully',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



class LoginAPIView(APIView):

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.validated_data['user']

            # login(request, user)
            auth_login(request, user)

            return Response(
                {
                    'message': 'Login successful',
                    'email': user.email,
                    'role': user.role,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
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
from rest_framework.parsers import (
    MultiPartParser,
    FormParser
)
class ProfileAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]
    
    parser_classes = [
        MultiPartParser,
        FormParser
    ]

    def get(self, request):

        serializer = ProfileSerializer(
            request.user,
            context={
                "request": request
            }
        )

        return Response({
            "success": True,
            "data": serializer.data
        })

    def put(self, request):

        serializer = ProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                "success": True,
                "message":
                    "Profile Updated Successfully",
                "data":
                    ProfileSerializer(
                        request.user,
                        context={
                            "request": request
                        }
                    ).data
            })

        return Response({
            "success": False,
            "errors": serializer.errors
        })



from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile_page(request):

    return render(
        request,
        "profile.html"
    )