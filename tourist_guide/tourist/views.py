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