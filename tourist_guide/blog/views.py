from django.shortcuts import render

# Create your views here.




from django.shortcuts import render

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


# def contact_us(request):
#     return render(
#         request,
#         "pages/contact_us.html"
#     )