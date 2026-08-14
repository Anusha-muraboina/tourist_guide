from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView

from tourist.models import (
    TourCategory,
    TourHighlight,
    TourInclude,
    TourExclude,
    ImportantInformation,
    Amenity
)

from blog.models import (
BlogCategory
)

from user.models  import Location

from .forms import (
    TourCategoryForm,
    TourHighlightForm,
    TourIncludeForm,
    TourExcludeForm,
    ImportantInformationForm,
    AmenityForm
)
from tourist.models import TourSchedule, TourPricing
from .forms import TourScheduleForm, TourPricingForm















from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print("Username:", username)
        print("Password:", password)

        user = authenticate(
            request,
            username=username,
            password=password
        )

        print("Authenticated User:", user)

        if user is not None:
            print("is_staff:", user.is_staff)

            if user.is_staff:
                login(request, user)
                return redirect("dashboard")

            messages.error(request, "You are not a staff user.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "tourist_admin/login.html")


def admin_logout(request):
    logout(request)
    return redirect("admin_login")


# def dashboard(request):
#     return render(
#         request,
#         "tourist_admin/dashboard.html"
#     )




# =====================================
# Dashboard
# =====================================

def dashboard(request):
    return render(request, "tourist_admin/dashboard.html")


# =====================================
# Base Delete View
# =====================================

class BaseDeleteView(View):
    model = None
    success_url = None

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        obj.delete()
        return redirect(self.success_url)


# =====================================
# TOUR CATEGORY
# =====================================

class TourCategoryListView(ListView):
    model = TourCategory
    template_name = "tourist_admin/category/list.html"
    context_object_name = "items"


class TourCategoryCreateView(CreateView):
    model = TourCategory
    form_class = TourCategoryForm
    template_name = "tourist_admin/category/form.html"
    success_url = reverse_lazy("tour_category_list")


class TourCategoryUpdateView(UpdateView):
    model = TourCategory
    form_class = TourCategoryForm
    template_name = "tourist_admin/category/form.html"
    success_url = reverse_lazy("tour_category_list")


class TourCategoryDeleteView(BaseDeleteView):
    model = TourCategory
    success_url = reverse_lazy("tour_category_list")


# =====================================
# TOUR HIGHLIGHT
# =====================================

class TourHighlightListView(ListView):
    model = TourHighlight
    template_name = "tourist_admin/tour_highlight/list.html"
    context_object_name = "items"


class TourHighlightCreateView(CreateView):
    model = TourHighlight
    form_class = TourHighlightForm
    template_name = "tourist_admin/tour_highlight/form.html"
    success_url = reverse_lazy("tour_highlight_list")


class TourHighlightUpdateView(UpdateView):
    model = TourHighlight
    form_class = TourHighlightForm
    template_name = "tourist_admin/tour_highlight/form.html"
    success_url = reverse_lazy("tour_highlight_list")


class TourHighlightDeleteView(BaseDeleteView):
    model = TourHighlight
    success_url = reverse_lazy("tour_highlight_list")


# =====================================
# TOUR INCLUDE
# =====================================

class TourIncludeListView(ListView):
    model = TourInclude
    template_name = "tourist_admin/tour_include/list.html"
    context_object_name = "items"


class TourIncludeCreateView(CreateView):
    model = TourInclude
    form_class = TourIncludeForm
    template_name = "tourist_admin/tour_include/form.html"
    success_url = reverse_lazy("tour_include_list")


class TourIncludeUpdateView(UpdateView):
    model = TourInclude
    form_class = TourIncludeForm
    template_name = "tourist_admin/tour_include/form.html"
    success_url = reverse_lazy("tour_include_list")


class TourIncludeDeleteView(BaseDeleteView):
    model = TourInclude
    success_url = reverse_lazy("tour_include_list")


# =====================================
# TOUR EXCLUDE
# =====================================

class TourExcludeListView(ListView):
    model = TourExclude
    template_name = "tourist_admin/tour_exclude/list.html"
    context_object_name = "items"


class TourExcludeCreateView(CreateView):
    model = TourExclude
    form_class = TourExcludeForm
    template_name = "tourist_admin/tour_exclude/form.html"
    success_url = reverse_lazy("tour_exclude_list")


class TourExcludeUpdateView(UpdateView):
    model = TourExclude
    form_class = TourExcludeForm
    template_name = "tourist_admin/tour_exclude/form.html"
    success_url = reverse_lazy("tour_exclude_list")


class TourExcludeDeleteView(BaseDeleteView):
    model = TourExclude
    success_url = reverse_lazy("tour_exclude_list")


# =====================================
# IMPORTANT INFORMATION
# =====================================

class ImportantInformationListView(ListView):
    model = ImportantInformation
    template_name = "tourist_admin/important_information/list.html"
    context_object_name = "items"


class ImportantInformationCreateView(CreateView):
    model = ImportantInformation
    form_class = ImportantInformationForm
    template_name = "tourist_admin/important_information/form.html"
    success_url = reverse_lazy("important_information_list")


class ImportantInformationUpdateView(UpdateView):
    model = ImportantInformation
    form_class = ImportantInformationForm
    template_name = "tourist_admin/important_information/form.html"
    success_url = reverse_lazy("important_information_list")


class ImportantInformationDeleteView(BaseDeleteView):
    model = ImportantInformation
    success_url = reverse_lazy("important_information_list")


# =====================================
# AMENITY
# =====================================

class AmenityListView(ListView):
    model = Amenity
    template_name = "tourist_admin/amenity/list.html"
    context_object_name = "items"


class AmenityCreateView(CreateView):
    model = Amenity
    form_class = AmenityForm
    template_name = "tourist_admin/amenity/form.html"
    success_url = reverse_lazy("amenity_list")


class AmenityUpdateView(UpdateView):
    model = Amenity
    form_class = AmenityForm
    template_name = "tourist_admin/amenity/form.html"
    success_url = reverse_lazy("amenity_list")


class AmenityDeleteView(BaseDeleteView):
    model = Amenity
    success_url = reverse_lazy("amenity_list")
    
    
    


# class TourScheduleListView(ListView):
#     model = TourSchedule
#     template_name = "tourist_admin/tour_schedule/list.html"
#     context_object_name = "items"


from django.views.generic import ListView
from tourist.models import TourSchedule, Tour


class TourScheduleListView(ListView):
    model = TourSchedule
    template_name = "tourist_admin/tour_schedule/list.html"
    context_object_name = "items"
    paginate_by = 10

    def get_queryset(self):
        queryset = TourSchedule.objects.select_related("tour")

        search = self.request.GET.get("search")
        tour = self.request.GET.get("tour")
        status = self.request.GET.get("status")

        if search:
            queryset = queryset.filter(
                tour__title__icontains=search
            )

        if tour:
            queryset = queryset.filter(
                tour_id=tour
            )

        if status == "1":
            queryset = queryset.filter(
                is_active=True
            )

        elif status == "0":
            queryset = queryset.filter(
                is_active=False
            )

        return queryset.order_by(
            "tour__title",
            "slot_position"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["tours"] = Tour.objects.filter(
            is_active=True
        ).order_by("title")

        context["search"] = self.request.GET.get("search", "")
        context["tour"] = self.request.GET.get("tour", "")
        context["status"] = self.request.GET.get("status", "")

        return context

class TourScheduleCreateView(CreateView):
    model = TourSchedule
    form_class = TourScheduleForm
    template_name = "tourist_admin/tour_schedule/form.html"
    success_url = reverse_lazy("tour_schedule_list")


class TourScheduleUpdateView(UpdateView):
    model = TourSchedule
    form_class = TourScheduleForm
    template_name = "tourist_admin/tour_schedule/form.html"
    success_url = reverse_lazy("tour_schedule_list")


class TourScheduleDeleteView(BaseDeleteView):
    model = TourSchedule
    success_url = reverse_lazy("tour_schedule_list")


######################################
# TOUR PRICING
######################################

# class TourPricingListView(ListView):
#     model = TourPricing
#     template_name = "tourist_admin/tour_pricing/list.html"
#     context_object_name = "items"
from django.views.generic import ListView
from tourist.models import TourPricing

class TourPricingListView(ListView):
    model = TourPricing
    template_name = "tourist_admin/tour_pricing/list.html"
    context_object_name = "items"
    paginate_by = 10

    def get_queryset(self):
        queryset = TourPricing.objects.select_related("tour")

        search = self.request.GET.get("search")
        person_type = self.request.GET.get("person_type")
        status = self.request.GET.get("status")

        if search:
            queryset = queryset.filter(
                tour__title__icontains=search
            )

        if person_type:
            queryset = queryset.filter(
                person_type=person_type
            )

        if status == "1":
            queryset = queryset.filter(is_active=True)

        elif status == "0":
            queryset = queryset.filter(is_active=False)

        return queryset

class TourPricingCreateView(CreateView):
    model = TourPricing
    form_class = TourPricingForm
    template_name = "tourist_admin/tour_pricing/form.html"
    success_url = reverse_lazy("tour_pricing_list")


class TourPricingUpdateView(UpdateView):
    model = TourPricing
    form_class = TourPricingForm
    template_name = "tourist_admin/tour_pricing/form.html"
    success_url = reverse_lazy("tour_pricing_list")


class TourPricingDeleteView(BaseDeleteView):
    model = TourPricing
    success_url = reverse_lazy("tour_pricing_list")
    
    
    
    
    
    
    
    
    
    
    
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView

from tourist.models import Tour, TourCategory
from .forms import TourForm


# =====================================
# Base Delete View
# =====================================

# class BaseDeleteView(View):
#     model = None
#     success_url = None

#     def get(self, request, pk):
#         obj = get_object_or_404(self.model, pk=pk)
#         obj.delete()
#         return redirect(self.success_url)


# =====================================
# TOUR LIST
# =====================================
class TourListView(ListView):
    model = Tour
    template_name = "tourist_admin/tour/list.html"
    context_object_name = "items"
    paginate_by = 10

    def get_queryset(self):
        queryset = (
            Tour.objects
            .select_related("category")
            .prefetch_related(
                "includes",
                "excludes",
                "highlights",
                "important_information",
                "amenities",
            )
        )

        search = self.request.GET.get("search")
        category = self.request.GET.get("category")
        status = self.request.GET.get("status")
        featured = self.request.GET.get("featured")

        if search:
            queryset = queryset.filter(title__icontains=search)

        if category:
            queryset = queryset.filter(category_id=category)

        if status == "1":
            queryset = queryset.filter(is_active=True)

        elif status == "0":
            queryset = queryset.filter(is_active=False)

        if featured == "1":
            queryset = queryset.filter(featured=True)

        elif featured == "0":
            queryset = queryset.filter(featured=False)

        return queryset.order_by("slot_position", "-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = TourCategory.objects.filter(is_active=True)

        context["search"] = self.request.GET.get("search", "")
        context["category"] = self.request.GET.get("category", "")
        context["status"] = self.request.GET.get("status", "")
        context["featured"] = self.request.GET.get("featured", "")

        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = (
            TourCategory.objects.filter(
                is_active=True
            )
        )

        context["search"] = self.request.GET.get("search", "")
        context["category"] = self.request.GET.get("category", "")
        context["status"] = self.request.GET.get("status", "")
        context["featured"] = self.request.GET.get("featured", "")

        return context


# =====================================
# TOUR CREATE
# =====================================

class TourCreateView(CreateView):
    model = Tour
    form_class = TourForm
    template_name = "tourist_admin/tour/form.html"
    success_url = reverse_lazy("tour_list")


# =====================================
# TOUR UPDATE
# =====================================

class TourUpdateView(UpdateView):
    model = Tour
    form_class = TourForm
    template_name = "tourist_admin/tour/form.html"
    success_url = reverse_lazy("tour_list")


# =====================================
# TOUR DELETE
# =====================================

class TourDeleteView(BaseDeleteView):
    model = Tour
    success_url = reverse_lazy("tour_list")
    
    
    
    
    
    
    
    
# from django.shortcuts import get_object_or_404, redirect
# from django.urls import reverse_lazy
# from django.views import View
# from django.views.generic import (
#     ListView,
#     CreateView,
#     UpdateView
# )

from contact.models import ContactUs
from .forms import ContactUsForm


# =====================================
# BASE DELETE VIEW
# =====================================

# class BaseDeleteView(View):

#     model = None
#     success_url = None

#     def get(self, request, pk):

#         obj = get_object_or_404(
#             self.model,
#             pk=pk
#         )

#         obj.delete()

#         return redirect(self.success_url)


# =====================================
# CONTACT US LIST
# =====================================

class ContactUsListView(ListView):

    model = ContactUs

    template_name = "tourist_admin/contact_us/list.html"

    context_object_name = "items"

    paginate_by = 10


    def get_queryset(self):

        queryset = ContactUs.objects.all()

        search = self.request.GET.get("search")

        status = self.request.GET.get("status")

        if search:

            queryset = queryset.filter(
                name__icontains=search
            ) | queryset.filter(
                email__icontains=search
            ) | queryset.filter(
                phone_number__icontains=search
            )

        if status == "1":

            queryset = queryset.filter(
                is_read=True
            )

        elif status == "0":

            queryset = queryset.filter(
                is_read=False
            )

        return queryset.order_by(
            "-created_at"
        )


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["search"] = self.request.GET.get(
            "search",
            ""
        )

        context["status"] = self.request.GET.get(
            "status",
            ""
        )

        return context


# =====================================
# CREATE
# =====================================

class ContactUsCreateView(CreateView):

    model = ContactUs

    form_class = ContactUsForm

    template_name = "tourist_admin/contact_us/form.html"

    success_url = reverse_lazy(
        "contact_us_list"
    )


# =====================================
# UPDATE
# =====================================

class ContactUsUpdateView(UpdateView):

    model = ContactUs

    form_class = ContactUsForm

    template_name = "tourist_admin/contact_us/form.html"

    success_url = reverse_lazy(
        "contact_us_list"
    )


# =====================================
# DELETE
# =====================================

class ContactUsDeleteView(BaseDeleteView):

    model = ContactUs

    success_url = reverse_lazy(
        "contact_us_list"
    )
    
    


from django.db.models import Q
# from django.shortcuts import get_object_or_404, redirect
# from django.urls import reverse_lazy
# from django.views import View
# from django.views.generic import (
#     ListView,
#     CreateView,
#     UpdateView,
# )

from coupon.models import Coupon
from .forms import CouponForm


# ==========================================
# Base Delete View
# ==========================================

# class BaseDeleteView(View):

#     model = None
#     success_url = None

#     def get(self, request, pk):

#         obj = get_object_or_404(
#             self.model,
#             pk=pk
#         )

#         obj.delete()

#         return redirect(
#             self.success_url
#         )


# ==========================================
# Coupon List
# ==========================================

class CouponListView(ListView):

    model = Coupon

    template_name = "tourist_admin/coupon/list.html"

    context_object_name = "items"

    paginate_by = 10


    def get_queryset(self):

        queryset = (
            Coupon.objects
            .select_related("tour")
            .all()
        )

        search = self.request.GET.get("search")

        discount_type = self.request.GET.get(
            "discount_type"
        )

        status = self.request.GET.get("status")


        if search:

            queryset = queryset.filter(

                Q(title__icontains=search) |

                Q(code__icontains=search) |

                Q(tour__title__icontains=search)

            )


        if discount_type:

            queryset = queryset.filter(
                discount_type=discount_type
            )


        if status == "1":

            queryset = queryset.filter(
                is_active=True
            )

        elif status == "0":

            queryset = queryset.filter(
                is_active=False
            )


        return queryset


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["search"] = self.request.GET.get(
            "search",
            ""
        )

        context["discount_type"] = self.request.GET.get(
            "discount_type",
            ""
        )

        context["status"] = self.request.GET.get(
            "status",
            ""
        )

        return context


# ==========================================
# Create Coupon
# ==========================================

class CouponCreateView(CreateView):

    model = Coupon

    form_class = CouponForm

    template_name = "tourist_admin/coupon/form.html"

    success_url = reverse_lazy(
        "coupon_list"
    )


# ==========================================
# Update Coupon
# ==========================================

class CouponUpdateView(UpdateView):

    model = Coupon

    form_class = CouponForm

    template_name = "tourist_admin/coupon/form.html"

    success_url = reverse_lazy(
        "coupon_list"
    )


# ==========================================
# Delete Coupon
# ==========================================

class CouponDeleteView(BaseDeleteView):

    model = Coupon

    success_url = reverse_lazy(
        "coupon_list"
    )
    
    
    


from rating.models import Rating
from .forms import RatingForm


# =====================================
# Rating List
# =====================================

class RatingListView(ListView):

    model = Rating

    template_name = "tourist_admin/rating/list.html"

    context_object_name = "items"

    paginate_by = 10

    def get_queryset(self):

        queryset = Rating.objects.select_related(
            "user",
            "tour"
        ).order_by(
            "-created_at"
        )

        search = self.request.GET.get(
            "search"
        )

        rating = self.request.GET.get(
            "rating"
        )

        status = self.request.GET.get(
            "status"
        )

        if search:

            queryset = queryset.filter(

                Q(user__email__icontains=search) |

                Q(user__username__icontains=search) |

                Q(tour__title__icontains=search) |

                Q(review__icontains=search)

            )

        if rating:

            queryset = queryset.filter(
                rating=rating
            )

        if status == "1":

            queryset = queryset.filter(
                active=True
            )

        elif status == "0":

            queryset = queryset.filter(
                active=False
            )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(
            **kwargs
        )

        context["search"] = self.request.GET.get(
            "search",
            ""
        )

        context["rating"] = self.request.GET.get(
            "rating",
            ""
        )

        context["status"] = self.request.GET.get(
            "status",
            ""
        )

        return context


# =====================================
# Create Rating
# =====================================

class RatingCreateView(CreateView):

    model = Rating

    form_class = RatingForm

    template_name = "tourist_admin/rating/form.html"

    success_url = reverse_lazy(
        "rating_list"
    )


# =====================================
# Update Rating
# =====================================

class RatingUpdateView(UpdateView):

    model = Rating

    form_class = RatingForm

    template_name = "tourist_admin/rating/form.html"

    success_url = reverse_lazy(
        "rating_list"
    )


# =====================================
# Delete Rating
# =====================================

class RatingDeleteView(BaseDeleteView):

    model = Rating

    success_url = reverse_lazy(
        "rating_list"
    )
    
    
# from django.views.generic import ListView
# from django.db.models import Q
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
)

from blog.models import BlogCategory, Blog
from .forms import BlogCategoryForm, BlogForm

from tourist_admin.views import BaseDeleteView


# ==========================================
# Blog Category List
# ==========================================

class BlogCategoryListView(ListView):

    model = BlogCategory

    template_name = "tourist_admin/blog/category_list.html"

    context_object_name = "items"

    paginate_by = 10

    def get_queryset(self):

        queryset = BlogCategory.objects.all()

        search = self.request.GET.get("search")

        status = self.request.GET.get("status")

        if search:

            queryset = queryset.filter(
                Q(name__icontains=search)
            )

        if status == "1":

            queryset = queryset.filter(
                is_active=True
            )

        elif status == "0":

            queryset = queryset.filter(
                is_active=False
            )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["search"] = self.request.GET.get(
            "search",
            ""
        )

        context["status"] = self.request.GET.get(
            "status",
            ""
        )

        return context


# ==========================================
# Blog Category Create
# ==========================================

class BlogCategoryCreateView(CreateView):

    model = BlogCategory

    form_class = BlogCategoryForm

    template_name = "tourist_admin/blog/category_form.html"

    success_url = reverse_lazy(
        "blog_category_list"
    )


# ==========================================
# Blog Category Update
# ==========================================

class BlogCategoryUpdateView(UpdateView):

    model = BlogCategory

    form_class = BlogCategoryForm

    template_name = "tourist_admin/blog/form.html"

    success_url = reverse_lazy(
        "blog_category_list"
    )


# ==========================================
# Blog Category Delete
# ==========================================

class BlogCategoryDeleteView(BaseDeleteView):

    model = BlogCategory

    success_url = reverse_lazy(
        "blog_category_list"
    )


# ==========================================
# Blog List
# ==========================================

class BlogListView(ListView):

    model = Blog

    template_name = "tourist_admin/blog/list.html"

    context_object_name = "items"

    paginate_by = 10

    def get_queryset(self):

        queryset = (
            Blog.objects
            .select_related("category")
            .all()
        )

        search = self.request.GET.get("search")

        category = self.request.GET.get("category")

        featured = self.request.GET.get("featured")

        status = self.request.GET.get("status")

        if search:

            queryset = queryset.filter(

                Q(title__icontains=search) |

                Q(author__icontains=search)

            )

        if category:

            queryset = queryset.filter(
                category_id=category
            )

        if featured == "1":

            queryset = queryset.filter(
                featured=True
            )

        elif featured == "0":

            queryset = queryset.filter(
                featured=False
            )

        if status == "1":

            queryset = queryset.filter(
                is_active=True
            )

        elif status == "0":

            queryset = queryset.filter(
                is_active=False
            )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["categories"] = BlogCategory.objects.filter(
            is_active=True
        )

        context["search"] = self.request.GET.get(
            "search",
            ""
        )

        context["category"] = self.request.GET.get(
            "category",
            ""
        )

        context["featured"] = self.request.GET.get(
            "featured",
            ""
        )

        context["status"] = self.request.GET.get(
            "status",
            ""
        )

        return context


# ==========================================
# Blog Create
# ==========================================

class BlogCreateView(CreateView):

    model = Blog

    form_class = BlogForm

    template_name = "tourist_admin/blog/form.html"

    success_url = reverse_lazy(
        "blog_list"
    )


# ==========================================
# Blog Update
# ==========================================

class BlogUpdateView(UpdateView):

    model = Blog

    form_class = BlogForm

    template_name = "tourist_admin/blog/form.html"

    success_url = reverse_lazy(
        "blog_list"
    )


# ==========================================
# Blog Delete
# ==========================================

class BlogDeleteView(BaseDeleteView):

    model = Blog

    success_url = reverse_lazy(
        "blog_list"
    )
    
    
    


# from django.db.models import Q
# from django.urls import reverse_lazy
# from django.views.generic import (
#     ListView,
#     CreateView,
#     UpdateView,
# )

from booking.models import CancelReason
from .forms import CancelReasonForm

from tourist_admin.views import BaseDeleteView


# ==========================================
# Cancel Reason List
# ==========================================

class CancelReasonListView(ListView):

    model = CancelReason

    template_name = "tourist_admin/cancel_reason/list.html"

    context_object_name = "items"

    paginate_by = 10

    def get_queryset(self):

        queryset = CancelReason.objects.all()

        search = self.request.GET.get("search")

        status = self.request.GET.get("status")

        if search:

            queryset = queryset.filter(

                Q(reason__icontains=search)

            )

        if status == "1":

            queryset = queryset.filter(
                is_active=True
            )

        elif status == "0":

            queryset = queryset.filter(
                is_active=False
            )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["search"] = self.request.GET.get(
            "search",
            ""
        )

        context["status"] = self.request.GET.get(
            "status",
            ""
        )

        return context


# ==========================================
# Create Cancel Reason
# ==========================================

class CancelReasonCreateView(CreateView):

    model = CancelReason

    form_class = CancelReasonForm

    template_name = "tourist_admin/cancel_reason/form.html"

    success_url = reverse_lazy(
        "cancel_reason_list"
    )


# ==========================================
# Update Cancel Reason
# ==========================================

class CancelReasonUpdateView(UpdateView):

    model = CancelReason

    form_class = CancelReasonForm

    template_name = "tourist_admin/cancel_reason/form.html"

    success_url = reverse_lazy(
        "cancel_reason_list"
    )


# ==========================================
# Delete Cancel Reason
# ==========================================

class CancelReasonDeleteView(BaseDeleteView):

    model = CancelReason

    success_url = reverse_lazy(
        "cancel_reason_list"
    )
    
    

from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
)

from booking.models import (
    BookingCancelComment,
    CancelReason,
)

from .forms import BookingCancelCommentForm

from tourist_admin.views import BaseDeleteView


# ==========================================
# Booking Cancel Comment List
# ==========================================

class BookingCancelCommentListView(ListView):

    model = BookingCancelComment

    template_name = "tourist_admin/booking_cancel_comment/list.html"

    context_object_name = "items"

    paginate_by = 10

    def get_queryset(self):

        queryset = (

            BookingCancelComment.objects

            .select_related(

                "user",

                "booking",

                "reason",

            )

            .all()

        )

        search = self.request.GET.get("search")

        reason = self.request.GET.get("reason")

        if search:

            queryset = queryset.filter(

                Q(comment__icontains=search) |

                Q(user__username__icontains=search) |

                Q(booking__booking_id__icontains=search)

            )

        if reason:

            queryset = queryset.filter(

                reason_id=reason

            )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["search"] = self.request.GET.get(

            "search",

            ""

        )

        context["reason"] = self.request.GET.get(

            "reason",

            ""

        )

        context["reasons"] = CancelReason.objects.filter(

            is_active=True

        )

        return context


# ==========================================
# Create
# ==========================================

class BookingCancelCommentCreateView(CreateView):

    model = BookingCancelComment

    form_class = BookingCancelCommentForm

    template_name = "tourist_admin/booking_cancel_comment/form.html"

    success_url = reverse_lazy(

        "booking_cancel_comment_list"

    )


# ==========================================
# Update
# ==========================================

class BookingCancelCommentUpdateView(UpdateView):

    model = BookingCancelComment

    form_class = BookingCancelCommentForm

    template_name = "tourist_admin/booking_cancel_comment/form.html"

    success_url = reverse_lazy(

        "booking_cancel_comment_list"

    )


# ==========================================
# Delete
# ==========================================

class BookingCancelCommentDeleteView(BaseDeleteView):

    model = BookingCancelComment

    success_url = reverse_lazy(

        "booking_cancel_comment_list"

    )
    
    
    


from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from .forms import TourPaymentPolicyForm
from booking.models import TourPaymentPolicy


class TourPaymentPolicyListView(ListView):
    model = TourPaymentPolicy
    template_name = "tourist_admin/policy/list.html"
    context_object_name = "items"
    paginate_by = 10

    def get_queryset(self):

        queryset = (
            TourPaymentPolicy.objects
            .select_related("tour")
            .order_by("tour__title")
        )

        search = self.request.GET.get("search")

        if search:
            queryset = queryset.filter(
                tour__title__icontains=search
            )

        return queryset


class TourPaymentPolicyCreateView(CreateView):
    model = TourPaymentPolicy
    form_class = TourPaymentPolicyForm
    template_name = "tourist_admin/policy/form.html"
    success_url = reverse_lazy("payment_policy_list")


class TourPaymentPolicyUpdateView(UpdateView):
    model = TourPaymentPolicy
    form_class = TourPaymentPolicyForm
    template_name = "tourist_admin/policy/form.html"
    success_url = reverse_lazy("payment_policy_list")


class TourPaymentPolicyDeleteView(BaseDeleteView):
    model = TourPaymentPolicy
    success_url = reverse_lazy("payment_policy_list")
    


# from django.db.models import Q
# from django.urls import reverse_lazy
# from django.views.generic import ListView, CreateView, UpdateView

# from .models import Location
from .forms import LocationForm
# from .views import BaseDeleteView


# ==========================================
# List
# ==========================================

class LocationListView(ListView):

    model = Location

    template_name = "tourist_admin/location/list.html"

    context_object_name = "items"

    paginate_by = 10

    def get_queryset(self):

        queryset = Location.objects.all()

        search = self.request.GET.get("search")

        state = self.request.GET.get("state")

        if search:

            queryset = queryset.filter(
                Q(country__icontains=search) |
                Q(state__icontains=search) |
                Q(district__icontains=search) |
                Q(city__icontains=search)
            )

        if state:

            queryset = queryset.filter(
                state__iexact=state
            )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["search"] = self.request.GET.get(
            "search",
            ""
        )

        context["state"] = self.request.GET.get(
            "state",
            ""
        )

        context["states"] = (
            Location.objects
            .values_list("state", flat=True)
            .distinct()
            .order_by("state")
        )

        return context


# ==========================================
# Create
# ==========================================

class LocationCreateView(CreateView):

    model = Location

    form_class = LocationForm

    template_name = "tourist_admin/location/form.html"

    success_url = reverse_lazy(
        "location_list"
    )


# ==========================================
# Update
# ==========================================

class LocationUpdateView(UpdateView):

    model = Location

    form_class = LocationForm

    template_name = "tourist_admin/location/form.html"

    success_url = reverse_lazy(
        "location_list"
    )


# ==========================================
# Delete
# ==========================================

class LocationDeleteView(BaseDeleteView):

    model = Location

    success_url = reverse_lazy(
        "location_list"
    )
    
    
    
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q

from .forms import UserForm

User = get_user_model()


class UserListView(ListView):

    model = User

    template_name = "tourist_admin/users/list.html"

    context_object_name = "items"

    paginate_by = 10

    def get_queryset(self):

        queryset = User.objects.prefetch_related(
            "locations"
        ).order_by("-created_at")

        search = self.request.GET.get("search")

        role = self.request.GET.get("role")

        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(phone_number__icontains=search)
            )

        if role:
            queryset = queryset.filter(role=role)

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["search"] = self.request.GET.get(
            "search",
            ""
        )

        context["role"] = self.request.GET.get(
            "role",
            ""
        )

        context["roles"] = User.ROLE_CHOICES

        return context


class UserDetailView(DetailView):

    model = User

    template_name = "tourist_admin/users/detail.html"

    context_object_name = "user_obj"


class UserUpdateView(UpdateView):

    model = User

    form_class = UserForm

    template_name = "tourist_admin/users/form.html"

    success_url = reverse_lazy("user_list")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone

from booking.models import Booking
from .forms import BookingForm


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


# ===================== LIST =====================
class BookingListView(StaffRequiredMixin, ListView):
    model = Booking
    template_name = "tourist_admin/bookings/list.html"
    context_object_name = "items"
    paginate_by = 15

    def get_queryset(self):
        queryset = Booking.objects.select_related(
            "tour", "tour__location", "guide", "user", "coupon_applied"
        ).order_by("-created_at")

        search = self.request.GET.get("search")
        status = self.request.GET.get("status")
        payment_status = self.request.GET.get("payment_status")
        payment_method = self.request.GET.get("payment_method")

        if search:
            queryset = queryset.filter(
                Q(booking_id__icontains=search) |
                Q(guest_name__icontains=search) |
                Q(guest_email__icontains=search) |
                Q(guest_phone__icontains=search) |
                Q(tour__title__icontains=search)
            )

        if status:
            queryset = queryset.filter(status=status)

        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)

        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("search", "")
        context["status"] = self.request.GET.get("status", "")
        context["payment_status"] = self.request.GET.get("payment_status", "")
        context["payment_method"] = self.request.GET.get("payment_method", "")

        context["status_choices"] = Booking.STATUS_CHOICES
        context["payment_status_choices"] = Booking.PAYMENT_STATUS_CHOICES
        context["payment_method_choices"] = Booking.PAYMENT_METHOD_CHOICES
        return context


# ===================== DETAIL =====================
class BookingDetailView(StaffRequiredMixin, DetailView):
    model = Booking
    template_name = "tourist_admin/bookings/detail.html"
    context_object_name = "booking"
    pk_url_kwarg = "pk"


# ===================== CREATE =====================
class BookingCreateView(StaffRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = "tourist_admin/bookings/form.html"
    success_url = reverse_lazy("booking_list")

    def form_valid(self, form):
        messages.success(self.request, "Booking created successfully")
        return super().form_valid(form)


# ===================== UPDATE =====================
class BookingUpdateView(StaffRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = "tourist_admin/bookings/form.html"
    success_url = reverse_lazy("booking_list")
    pk_url_kwarg = "pk"

    def form_valid(self, form):
        messages.success(self.request, "Booking updated successfully")
        return super().form_valid(form)


# ===================== DELETE =====================
class BookingDeleteView(StaffRequiredMixin, DeleteView):
    model = Booking
    template_name = "tourist_admin/bookings/confirm_delete.html"
    success_url = reverse_lazy("booking_list")
    pk_url_kwarg = "pk"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Booking deleted successfully")
        return super().delete(request, *args, **kwargs)


# ===================== QUICK STATUS CHANGE =====================
class BookingStatusUpdateView(StaffRequiredMixin, UpdateView):
    model = Booking
    fields = ["status"]
    pk_url_kwarg = "pk"

    def post(self, request, *args, **kwargs):
        booking = self.get_object()
        new_status = request.POST.get("status")

        if new_status in dict(Booking.STATUS_CHOICES):
            old_status = booking.status
            booking.status = new_status

            if new_status == "cancelled":
                booking.cancelled_at = timezone.now()
                booking.cancelled_by = "admin"
                if booking.payment_status in ["paid", "partial"]:
                    booking.payment_status = "failed"

            booking.save()

            if old_status != new_status:
                try:
                    booking.send_booking_email(new_status)
                except Exception:
                    pass

            messages.success(request, f"Status updated to {new_status}")
        else:
            messages.error(request, "Invalid status")

        return redirect("booking_detail", pk=booking.pk)