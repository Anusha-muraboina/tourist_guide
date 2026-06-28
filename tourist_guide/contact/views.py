from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import ContactUs

from django.http import HttpResponse
# def contact(request):
#     return HttpResponse("Welcome to Tourist Guide")



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactUsSerializer


class ContactUsAPIView(APIView):

    # permission_classes = []

    def post(self, request):

        serializer = ContactUsSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Your message has been sent successfully."
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
        


from django.shortcuts import render
def contact(request):
    return render(
        request,
        "pages/contact_us.html"
    )