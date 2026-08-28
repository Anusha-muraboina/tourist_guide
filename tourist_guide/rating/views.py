from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
# Create your views here.
def rating(request):
    return HttpResponse("Welcome to Tourist Guide")
    # render(request )
    
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rating.models import Rating
from .serializers import RatingCreateSerializer
from booking.models import Booking


class AddRatingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = RatingCreateSerializer(
            data=request.data
        )

        if serializer.is_valid():

            tour = serializer.validated_data["tour"]

            # ✅ Check completed booking
            booking_exists = Booking.objects.filter(
                user=request.user,
                tour=tour,
                status="completed"   # not booking_status
            ).exists()

            if not booking_exists:
                return Response(
                    {
                        "success": False,
                        "message": "You can rate only after completing the tour."
                    },
                    status=400
                )

            # ✅ Prevent duplicate rating
            if Rating.objects.filter(
                user=request.user,
                tour=tour
            ).exists():

                return Response(
                    {
                        "success": False,
                        "message": "You already rated this tour."
                    },
                    status=400
                )

            serializer.save(
                user=request.user
            )

            return Response(
                {
                    "success": True,
                    "message": "Rating added successfully."
                }
            )

        return Response(
            serializer.errors,
            status=400
        )