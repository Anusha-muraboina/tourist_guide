from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
# Create your views here.
def user(request):
    return HttpResponse("Welcome to Tourist Guide")
    render(request )