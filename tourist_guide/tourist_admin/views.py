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

def dashboard(request):
    return render(
        request,
        "tourist_admin/dashboard.html"
    )




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