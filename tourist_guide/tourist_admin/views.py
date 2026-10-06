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
    Amenity,
    Itinerary
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
    AmenityForm,
    TourItineraryForm
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

# def dashboard(request):
#     return render(request, "tourist_admin/dashboard.html")



from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum

from tourist.models import Tour, TourCategory, TourSchedule


@login_required
def dashboard(request):

    # ============================================================
    # TOUR COUNTS
    # ============================================================

    total_tours = Tour.objects.count()

    active_tours = Tour.objects.filter(
        is_active=True
    ).count()

    inactive_tours = Tour.objects.filter(
        is_active=False
    ).count()

    featured_tours = Tour.objects.filter(
        featured=True,
        is_active=True
    ).count()


    # ============================================================
    # CATEGORIES
    # ============================================================

    total_categories = TourCategory.objects.count()

    active_categories = TourCategory.objects.filter(
        is_active=True
    ).count()


    # ============================================================
    # TODAY'S / AVAILABLE SLOTS
    #
    # TourSchedule does not have a date field in your current
    # model, so this represents the total available slots from
    # active schedules.
    # ============================================================

    today_slots = (
        TourSchedule.objects
        .filter(
            is_active=True,
            tour__is_active=True
        )
        .aggregate(
            total=Sum("available_slots")
        )
        .get("total")
        or 0
    )


    # ============================================================
    # RECENT TOURS
    # ============================================================

    recent_tours = (
        Tour.objects
        .select_related(
            "category",
            "location",
        )
        .prefetch_related(
            "images",
            "pricing",
        )
        .order_by("-created_at")[:8]
    )


    # ============================================================
    # CONTEXT
    # ============================================================

    context = {

        # Tour statistics
        "total_tours": total_tours,
        "active_tours": active_tours,
        "inactive_tours": inactive_tours,
        "featured_tours": featured_tours,

        # Category statistics
        "total_categories": total_categories,
        "active_categories": active_categories,

        # Schedule statistics
        "today_slots": today_slots,

        # Recent tours
        "recent_tours": recent_tours,
    }


    return render(
        request,
        "tourist_admin/dashboard.html",
        context
    )

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
# TOUR Itinerary
# =====================================

class TourItineraryListView(ListView):
    model = Itinerary
    template_name = "tourist_admin/tour_itirenary/list.html"
    context_object_name = "items"


class TourItineraryCreateView(CreateView):
    model = Itinerary
    form_class = TourItineraryForm
    template_name = "tourist_admin/tour_itirenary/form.html"
    success_url = reverse_lazy("tour_itirenary_list")


class TourItineraryUpdateView(UpdateView):
    model = Itinerary
    form_class = TourItineraryForm
    template_name = "tourist_admin/tour_itirenary/form.html"
    success_url = reverse_lazy("tour_itirenary_list")


class TourItineraryDeleteView(BaseDeleteView):
    model = Itinerary
    success_url = reverse_lazy("tour_itirenary_list")


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


class TourPricingListView(ListView):
    model = TourPricing
    template_name = "tourist_admin/tour_pricing/list.html"
    context_object_name = "items"
    paginate_by = 10

    def get_queryset(self):
        queryset = TourPricing.objects.select_related("tour").order_by("-id")

        search = self.request.GET.get("search", "").strip()
        group_type = self.request.GET.get("group_type", "").strip()
        status = self.request.GET.get("status", "").strip()

        if search:
            queryset = queryset.filter(
                tour__title__icontains=search
            )

        if group_type:
            queryset = queryset.filter(
                group_type=group_type
            )

        if status == "1":
            queryset = queryset.filter(is_active=True)

        elif status == "0":
            queryset = queryset.filter(is_active=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search"] = self.request.GET.get("search", "")
        context["group_type"] = self.request.GET.get("group_type", "")
        context["status"] = self.request.GET.get("status", "")

        context["group_type_choices"] = TourPricing.GROUP_TYPE_CHOICES

        return context


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
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
)
from django.db import transaction

from tourist.models import (
    Tour,
    TourCategory,
    TourImage,
)

from .forms import (
    TourForm,
)


# ============================================================
# TOUR LIST# ============================================================
from django.db.models import Q, Prefetch
from django.views.generic import ListView

# from .models import (
#     Tour,
#     TourCategory,
#     TourImage,
# )


class TourListView(ListView):

    model = Tour

    template_name = "tourist_admin/tour/list.html"

    context_object_name = "items"

    paginate_by = 10

    # ========================================================
    # QUERYSET
    # ========================================================

    def get_queryset(self):

        queryset = (
            Tour.objects
            .select_related(
                "category",
                "location",
            )
            .prefetch_related(

                # ==================================================
                # IMAGES
                # Primary image first
                # ==================================================

                Prefetch(
                    "images",
                    queryset=(
                        TourImage.objects
                        .order_by(
                            "-is_primary",
                            "created_at",
                        )
                    ),
                ),

                # ==================================================
                # M2M
                # ==================================================

                "includes",
                "excludes",
                "itinerary",
                "highlights",
                "important_information",
                "amenities",

                # ==================================================
                # PRICING
                # ==================================================

                "pricing",

                # ==================================================
                # SCHEDULES
                # ==================================================

                "schedules",
            )
        )

        # ========================================================
        # SEARCH
        # ========================================================

        search = (
            self.request.GET.get(
                "search",
                "",
            )
            .strip()
        )

        # ========================================================
        # FILTERS
        # ========================================================

        category = (
            self.request.GET.get(
                "category",
                "",
            )
            .strip()
        )

        status = (
            self.request.GET.get(
                "status",
                "",
            )
            .strip()
        )

        featured = (
            self.request.GET.get(
                "featured",
                "",
            )
            .strip()
        )

        # ========================================================
        # SEARCH
        # ========================================================
        #
        # Search supports:
        #
        # 1. Tour title
        # 2. Place / Monument
        # 3. City
        # 4. District
        # 5. State
        # 6. Country
        #
        # Location.architecture = actual place/monument name
        #
        # Example:
        #
        # Charminar
        # Golconda Fort
        # Hyderabad
        # Telangana
        #
        # ========================================================

        if search:

            queryset = queryset.filter(

                Q(title__icontains=search)

                |

                Q(
                    location__architecture__icontains=search
                )

                |

                Q(
                    location__city__icontains=search
                )

                |

                Q(
                    location__district__icontains=search
                )

                |

                Q(
                    location__state__icontains=search
                )

                |

                Q(
                    location__country__icontains=search
                )

            )

        # ========================================================
        # CATEGORY
        # ========================================================

        if category:

            queryset = queryset.filter(
                category_id=category
            )

        # ========================================================
        # ACTIVE STATUS
        # ========================================================

        if status == "1":

            queryset = queryset.filter(
                is_active=True
            )

        elif status == "0":

            queryset = queryset.filter(
                is_active=False
            )

        # ========================================================
        # FEATURED
        # ========================================================

        if featured == "1":

            queryset = queryset.filter(
                featured=True
            )

        elif featured == "0":

            queryset = queryset.filter(
                featured=False
            )

        # ========================================================
        # REMOVE DUPLICATES
        # ========================================================

        queryset = queryset.distinct()

        # ========================================================
        # ORDER
        # ========================================================

        return queryset.order_by(
            "slot_position",
            "-created_at",
        )

    # ========================================================
    # CONTEXT
    # ========================================================

    def get_context_data(
        self,
        **kwargs,
    ):

        context = super().get_context_data(
            **kwargs
        )

        # ========================================================
        # CATEGORIES
        # ========================================================

        context["categories"] = (
            TourCategory.objects
            .filter(
                is_active=True
            )
            .order_by(
                "slot_position",
                "name",
            )
        )

        # ========================================================
        # CURRENT SEARCH
        # ========================================================

        context["search"] = (
            self.request.GET.get(
                "search",
                "",
            )
        )

        # ========================================================
        # CURRENT CATEGORY
        # ========================================================

        context["category"] = (
            self.request.GET.get(
                "category",
                "",
            )
        )

        # ========================================================
        # CURRENT STATUS
        # ========================================================

        context["status"] = (
            self.request.GET.get(
                "status",
                "",
            )
        )

        # ========================================================
        # CURRENT FEATURED
        # ========================================================

        context["featured"] = (
            self.request.GET.get(
                "featured",
                "",
            )
        )

        # ========================================================
        # STATISTICS
        # ========================================================

        context["total_tours"] = (
            Tour.objects.count()
        )

        context["active_count"] = (
            Tour.objects
            .filter(
                is_active=True
            )
            .count()
        )

        context["inactive_count"] = (
            Tour.objects
            .filter(
                is_active=False
            )
            .count()
        )

        context["featured_count"] = (
            Tour.objects
            .filter(
                featured=True
            )
            .count()
        )

        # ========================================================
        # RETURN
        # ========================================================

        return context


# ============================================================
# TOUR CREATE
# ============================================================

# class TourCreateView(CreateView):

#     model = Tour

#     form_class = TourForm

#     template_name = (
#         "tourist_admin/tour/form.html"
#     )

#     success_url = reverse_lazy(
#         "tour_list"
#     )

#     def form_valid(self, form):

#         # ====================================================
#         # SAVE TOUR
#         # ====================================================

#         self.object = form.save()

#         # ====================================================
#         # SAVE MULTIPLE IMAGES
#         # ====================================================

#         images = self.request.FILES.getlist(
#             "tour_images"
#         )

#         for index, image in enumerate(images):

#             TourImage.objects.create(
#                 tour=self.object,
#                 image=image,
#                 is_primary=(index == 0),
#             )

#         return redirect(
#             self.success_url
#         )


# # ============================================================
# # TOUR UPDATE
# # ============================================================

# class TourUpdateView(UpdateView):

#     model = Tour

#     form_class = TourForm

#     template_name = (
#         "tourist_admin/tour/form.html"
#     )

#     success_url = reverse_lazy(
#         "tour_list"
#     )

#     def get_context_data(
#         self,
#         **kwargs
#     ):

#         context = super().get_context_data(
#             **kwargs
#         )

#         context["tour_images"] = (
#             self.object.images.all()
#             .order_by(
#                 "-is_primary",
#                 "created_at",
#             )
#         )

#         return context

#     @transaction.atomic
#     def form_valid(self, form):

#         # ====================================================
#         # SAVE TOUR
#         # ====================================================

#         self.object = form.save()

#         # ====================================================
#         # NEW IMAGES
#         # ====================================================

#         images = self.request.FILES.getlist(
#             "tour_images"
#         )

#         existing_images = self.object.images.exists()

#         for index, image in enumerate(images):

#             TourImage.objects.create(
#                 tour=self.object,
#                 image=image,
#                 is_primary=(
#                     not existing_images
#                     and index == 0
#                 ),
#             )

#         return redirect(
#             self.success_url
#         )
from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView



class TourCreateView(CreateView):
    model = Tour
    form_class = TourForm
    template_name = "tourist_admin/tour/form.html"
    success_url = reverse_lazy("tour_list")

    @transaction.atomic
    def form_valid(self, form):
        self.object = form.save()

        # Save pricing
        self.save_pricing()

        # Save all uploaded images
        self.save_images()

        messages.success(
            self.request,
            "Tour created successfully."
        )

        return redirect(self.success_url)

    def save_pricing(self):
        pricing_data = [
            {
                "group_type": "upto_9",
                "group_members": "Up to 9 members",
                "field": "price_upto_9",
            },
            {
                "group_type": "10_20",
                "group_members": "10 - 20 members",
                "field": "price_10_20",
            },
            {
                "group_type": "20_50",
                "group_members": "20 - 50 members",
                "field": "price_20_50",
            },
        ]

        for data in pricing_data:
            value = self.request.POST.get(data["field"], "").strip()

            if not value:
                continue

            try:
                price = Decimal(value)
            except Exception:
                continue

            if price < 0:
                continue

            TourPricing.objects.create(
                tour=self.object,
                group_type=data["group_type"],
                group_members=data["group_members"],
                group_price=price,
                is_active=True,
            )

    def save_images(self):
        """
        Save ALL selected images.

        Frontend sends:
            primary_image = index of selected primary image

        Example:
            primary_image = 2

        means the third uploaded image becomes primary.
        """

        images = self.request.FILES.getlist("tour_images")

        if not images:
            return

        primary_index = self.request.POST.get("primary_image", "0")

        try:
            primary_index = int(primary_index)
        except (TypeError, ValueError):
            primary_index = 0

        # Safety check
        if primary_index < 0 or primary_index >= len(images):
            primary_index = 0

        for index, image in enumerate(images):

            TourImage.objects.create(
                tour=self.object,
                image=image,
                is_primary=(index == primary_index),
            )


class TourUpdateView(UpdateView):
    model = Tour
    form_class = TourForm
    template_name = "tourist_admin/tour/form.html"
    success_url = reverse_lazy("tour_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["tour_images"] = (
            self.object.images
            .all()
            .order_by("-is_primary", "created_at")
        )

        pricing = self.object.pricing.filter(is_active=True)

        context["pricing_upto_9"] = (
            pricing.filter(group_type="upto_9").first()
        )

        context["pricing_10_20"] = (
            pricing.filter(group_type="10_20").first()
        )

        context["pricing_20_50"] = (
            pricing.filter(group_type="20_50").first()
        )

        return context

    @transaction.atomic
    def form_valid(self, form):
        self.object = form.save()

        # Update pricing
        self.update_pricing()

        # Save newly uploaded images
        self.save_new_images()

        # Change primary image if selected
        self.update_primary_image()

        messages.success(
            self.request,
            "Tour updated successfully."
        )

        return redirect(self.success_url)

    def update_pricing(self):
        pricing_data = [
            {
                "group_type": "upto_9",
                "group_members": "Up to 9 members",
                "field": "price_upto_9",
            },
            {
                "group_type": "10_20",
                "group_members": "10 - 20 members",
                "field": "price_10_20",
            },
            {
                "group_type": "20_50",
                "group_members": "20 - 50 members",
                "field": "price_20_50",
            },
        ]

        for data in pricing_data:

            value = self.request.POST.get(
                data["field"],
                ""
            ).strip()

            existing = TourPricing.objects.filter(
                tour=self.object,
                group_type=data["group_type"]
            ).first()

            if not value:

                if existing:
                    existing.is_active = False
                    existing.save(
                        update_fields=["is_active"]
                    )

                continue

            try:
                price = Decimal(value)
            except Exception:
                continue

            if price < 0:
                continue

            if existing:

                existing.group_members = data["group_members"]
                existing.group_price = price
                existing.is_active = True

                existing.save()

            else:

                TourPricing.objects.create(
                    tour=self.object,
                    group_type=data["group_type"],
                    group_members=data["group_members"],
                    group_price=price,
                    is_active=True,
                )

    def save_new_images(self):
        """
        Save all newly uploaded images.

        Do NOT automatically make the first new image primary
        when an existing primary image already exists.
        """

        images = self.request.FILES.getlist("tour_images")

        if not images:
            return

        existing_primary = self.object.images.filter(
            is_primary=True
        ).exists()

        primary_index = self.request.POST.get(
            "primary_image",
            ""
        )

        try:
            primary_index = int(primary_index)
        except (TypeError, ValueError):
            primary_index = None

        for index, image in enumerate(images):

            make_primary = False

            # User selected one of the NEW images as primary
            if (
                primary_index is not None
                and index == primary_index
            ):
                make_primary = True

                # Remove primary from old image
                TourImage.objects.filter(
                    tour=self.object
                ).update(is_primary=False)

            # If there is no primary image at all,
            # first uploaded image becomes primary.
            elif (
                not existing_primary
                and index == 0
            ):
                make_primary = True

            TourImage.objects.create(
                tour=self.object,
                image=image,
                is_primary=make_primary,
            )

            if make_primary:
                existing_primary = True

    def update_primary_image(self):
        """
        Handles selecting an EXISTING image as primary
        from the same tour form.

        No separate URL.
        No separate page.
        No redirect until the normal Update button.
        """

        existing_primary_id = self.request.POST.get(
            "existing_primary_image"
        )

        if not existing_primary_id:
            return

        try:
            existing_primary_id = int(existing_primary_id)
        except (TypeError, ValueError):
            return

        image = TourImage.objects.filter(
            id=existing_primary_id,
            tour=self.object
        ).first()

        if not image:
            return

        TourImage.objects.filter(
            tour=self.object
        ).update(is_primary=False)

        image.is_primary = True
        image.save(update_fields=["is_primary"])

# ============================================================
# TOUR DELETE
# ============================================================

class TourDeleteView(BaseDeleteView):

    model = Tour

    success_url = reverse_lazy(
        "tour_list"
    )


# ============================================================
# DELETE TOUR IMAGE
# ============================================================

def delete_tour_image(
    request,
    pk
):

    image = get_object_or_404(
        TourImage,
        pk=pk,
    )

    tour_id = image.tour_id

    image.delete()

    return redirect(
        "tour_update",
        pk=tour_id,
    )


# ============================================================
# SET PRIMARY IMAGE
# ============================================================

def set_primary_tour_image(
    request,
    pk
):

    image = get_object_or_404(
        TourImage,
        pk=pk,
    )

    TourImage.objects.filter(
        tour=image.tour
    ).update(
        is_primary=False
    )

    image.is_primary = True

    image.save(
        update_fields=[
            "is_primary"
        ]
    )

    return redirect(
        "tour_update",
        pk=image.tour_id,
    )
    
    
    
    
    
    
    
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
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

# from .models import Location
# from .forms import LocationForm


# ============================================================
# LOCATION LIST
# ============================================================

class LocationListView(ListView):

    model = Location

    template_name = "tourist_admin/location/list.html"

    context_object_name = "items"

    paginate_by = 10

    def get_queryset(self):

        queryset = (
            Location.objects
            .all()
            .order_by(
                "country",
                "state",
                "district",
                "city",
                "architecture",
            )
        )

        search = self.request.GET.get(
            "search",
            ""
        ).strip()

        state = self.request.GET.get(
            "state",
            ""
        ).strip()

        if search:

            queryset = queryset.filter(

                Q(country__icontains=search)
                |
                Q(state__icontains=search)
                |
                Q(district__icontains=search)
                |
                Q(city__icontains=search)
                |
                Q(architecture__icontains=search)

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
            .values_list(
                "state",
                flat=True
            )
            .distinct()
            .order_by("state")
        )

        context["active_count"] = (
            Location.objects
            .filter(is_active=True)
            .count()
        )

        context["inactive_count"] = (
            Location.objects
            .filter(is_active=False)
            .count()
        )

        context["total_locations"] = (
            Location.objects.count()
        )

        return context


# ============================================================
# LOCATION CREATE
# ============================================================

class LocationCreateView(CreateView):

    model = Location

    form_class = LocationForm

    template_name = "tourist_admin/location/form.html"

    success_url = reverse_lazy(
        "location_list"
    )


# ============================================================
# LOCATION UPDATE
# ============================================================

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

from django.contrib.auth import get_user_model
from django.views.generic import ListView
from django.db.models import Q

User = get_user_model()


class UserListView(ListView):
    model = User
    template_name = "tourist_admin/users/list.html"
    context_object_name = "items"
    paginate_by = 10

    def get_queryset(self):
        queryset = (
            User.objects
            .prefetch_related("locations")
            .order_by("-created_at")
        )

        search = self.request.GET.get("search", "").strip()
        role = self.request.GET.get("role", "").strip()

        # ==========================
        # SEARCH
        # ==========================
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search)
                | Q(email__icontains=search)
                | Q(phone_number__icontains=search)
            )

        # ==========================
        # ROLE FILTER
        # ==========================
        if role in ["tourist", "guide", "admin"]:
            queryset = queryset.filter(role=role)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search"] = self.request.GET.get(
            "search",
            ""
        )

        context["selected_role"] = self.request.GET.get(
            "role",
            ""
        )

        # Role dropdown
        context["roles"] = User.ROLE_CHOICES

        # ==========================
        # ROLE COUNTS
        # ==========================
        context["total_users"] = User.objects.count()

        context["tourist_count"] = User.objects.filter(
            role="tourist"
        ).count()

        context["guide_count"] = User.objects.filter(
            role="guide"
        ).count()

        context["admin_count"] = User.objects.filter(
            role="admin"
        ).count()

        return context
    
from django.contrib.auth import get_user_model
from django.views.generic import DetailView

User = get_user_model()


# class UserDetailView(DetailView):
#     model = User
#     template_name = "tourist_admin/users/detail.html"
#     context_object_name = "user_obj"

#     def get_queryset(self):
#         return (
#             User.objects
#             .prefetch_related("locations")
#             .select_related("guide_profile")
#         )

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         user_obj = self.object

#         # GuideProfile exists only for guide users
#         if user_obj.role == "guide":
#             try:
#                 context["guide_profile"] = user_obj.guide_profile
#             except user_obj.guide_profile.RelatedObjectDoesNotExist:
#                 context["guide_profile"] = None
#         else:
#             context["guide_profile"] = None

#         return context


class UserDetailView(DetailView):
    model = User
    template_name = "tourist_admin/users/detail.html"
    context_object_name = "user_obj"

    def get_queryset(self):
        return (
            User.objects
            .prefetch_related("locations")
            .select_related("guide_profile")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_obj = self.object

        if user_obj.role == "guide":
            try:
                context["guide_profile"] = user_obj.guide_profile
            except user_obj.guide_profile.RelatedObjectDoesNotExist:
                context["guide_profile"] = None
        else:
            context["guide_profile"] = None

        # Selected locations / architecture
        context["user_locations"] = user_obj.locations.all()

        return context

    
from django.contrib.auth import get_user_model
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.db import transaction

from .forms import UserForm
from user.models import GuideProfile, Location

User = get_user_model()


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = "tourist_admin/users/form.html"
    success_url = reverse_lazy("user_list")

    def get_queryset(self):
        return (
            User.objects
            .prefetch_related("locations")
            .select_related("guide_profile")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # All active locations for architecture/place selection
        context["locations"] = Location.objects.filter(
            is_active=True
        ).order_by(
            "state",
            "district",
            "city",
            "architecture",
        )

        if self.object.role == "guide":
            try:
                context["guide_profile"] = self.object.guide_profile
            except GuideProfile.DoesNotExist:
                context["guide_profile"] = None
        else:
            context["guide_profile"] = None

        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()

        if form.is_valid():

            user = form.save()

            # ==========================================
            # UPDATE USER LOCATIONS / ARCHITECTURE
            # ==========================================

            location_ids = request.POST.getlist("locations")

            if location_ids:
                locations = Location.objects.filter(
                    id__in=location_ids,
                    is_active=True
                )

                user.locations.set(locations)

            else:
                user.locations.clear()

            # ==========================================
            # GUIDE PROFILE
            # ==========================================

            if user.role == "guide":

                try:
                    guide_profile = user.guide_profile
                except GuideProfile.DoesNotExist:
                    guide_profile = GuideProfile(user=user)

                # Bio
                guide_profile.bio = request.POST.get(
                    "bio",
                    ""
                ).strip()

                # Experience
                experience = request.POST.get(
                    "experience_years",
                    "0"
                )

                try:
                    guide_profile.experience_years = int(
                        experience or 0
                    )
                except (ValueError, TypeError):
                    guide_profile.experience_years = 0

                # Languages
                guide_profile.languages = request.POST.get(
                    "languages",
                    ""
                ).strip()

                # Aadhaar Front
                if "aadhaar_front" in request.FILES:
                    guide_profile.aadhaar_front = (
                        request.FILES["aadhaar_front"]
                    )

                # Aadhaar Back
                if "aadhaar_back" in request.FILES:
                    guide_profile.aadhaar_back = (
                        request.FILES["aadhaar_back"]
                    )

                # Certificates
                if "certificates" in request.FILES:
                    guide_profile.certificates = (
                        request.FILES["certificates"]
                    )

                # Verification status
                guide_profile.verification_status = request.POST.get(
                    "verification_status",
                    guide_profile.verification_status or "pending"
                )

                # Rejection reason
                guide_profile.rejection_reason = request.POST.get(
                    "rejection_reason",
                    ""
                ).strip()

                guide_profile.save()

            return self.form_valid(form)

        return self.form_invalid(form)  
    
    
    
    
    
    
    
    
    
    
# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy
# from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.contrib import messages
# from django.shortcuts import redirect
# from django.utils import timezone

from booking.models import Booking
from .forms import BookingForm


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone




# =========================================================
# STAFF MIXIN
# =========================================================

class StaffRequiredMixin(
    LoginRequiredMixin,
    UserPassesTestMixin
):

    def test_func(self):

        return (
            self.request.user.is_staff
            or self.request.user.is_superuser
        )


# =========================================================
# BOOKING LIST
# =========================================================

class BookingListView(
    StaffRequiredMixin,
    ListView
):

    model = Booking

    template_name = (
        "tourist_admin/bookings/list.html"
    )

    context_object_name = "items"

    paginate_by = 15


    def get_queryset(self):

        queryset = (
            Booking.objects
            .select_related(
                "tour",
                "tour__location",
                "guide",
                "user",
                "coupon_applied",
                "pricing",
            )
            .order_by("-created_at")
        )


        search = self.request.GET.get(
            "search",
            ""
        ).strip()

        status = self.request.GET.get(
            "status",
            ""
        ).strip()

        payment_status = self.request.GET.get(
            "payment_status",
            ""
        ).strip()

        payment_method = self.request.GET.get(
            "payment_method",
            ""
        ).strip()


        # SEARCH

        if search:

            queryset = queryset.filter(

                Q(booking_id__icontains=search)

                |

                Q(guest_name__icontains=search)

                |

                Q(guest_email__icontains=search)

                |

                Q(guest_phone__icontains=search)

                |

                Q(tour__title__icontains=search)

            )


        # STATUS

        if status:

            queryset = queryset.filter(
                status=status
            )


        # PAYMENT STATUS

        if payment_status:

            queryset = queryset.filter(
                payment_status=payment_status
            )


        # PAYMENT METHOD

        if payment_method:

            queryset = queryset.filter(
                payment_method=payment_method
            )


        return queryset


    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )


        context["search"] = self.request.GET.get(
            "search",
            ""
        )

        context["status"] = self.request.GET.get(
            "status",
            ""
        )

        context["payment_status"] = (
            self.request.GET.get(
                "payment_status",
                ""
            )
        )

        context["payment_method"] = (
            self.request.GET.get(
                "payment_method",
                ""
            )
        )


        context["status_choices"] = (
            Booking.STATUS_CHOICES
        )

        context["payment_status_choices"] = (
            Booking.PAYMENT_STATUS_CHOICES
        )

        context["payment_method_choices"] = (
            Booking.PAYMENT_METHOD_CHOICES
        )


        return context


# =========================================================
# BOOKING DETAIL
# =========================================================

class BookingDetailView(
    StaffRequiredMixin,
    DetailView
):

    model = Booking

    template_name = (
        "tourist_admin/bookings/detail.html"
    )

    context_object_name = "booking"

    pk_url_kwarg = "pk"


# =========================================================
# BOOKING CREATE
# =========================================================

class BookingCreateView(
    StaffRequiredMixin,
    CreateView
):

    model = Booking

    form_class = BookingForm

    template_name = (
        "tourist_admin/bookings/form.html"
    )

    success_url = reverse_lazy(
        "booking_list"
    )


    def form_valid(self, form):

        messages.success(
            self.request,
            "Booking created successfully."
        )

        return super().form_valid(form)


# =========================================================
# BOOKING UPDATE
# =========================================================

class BookingUpdateView(
    StaffRequiredMixin,
    UpdateView
):

    model = Booking

    form_class = BookingForm

    template_name = (
        "tourist_admin/bookings/form.html"
    )

    success_url = reverse_lazy(
        "booking_list"
    )

    pk_url_kwarg = "pk"


    def form_valid(self, form):

        messages.success(
            self.request,
            "Booking updated successfully."
        )

        return super().form_valid(form)


# =========================================================
# BOOKING DELETE
# =========================================================

class BookingDeleteView(
    StaffRequiredMixin,
    DeleteView
):

    model = Booking

    template_name = (
        "tourist_admin/bookings/confirm_delete.html"
    )

    success_url = reverse_lazy(
        "booking_list"
    )

    pk_url_kwarg = "pk"


    def delete(
        self,
        request,
        *args,
        **kwargs
    ):

        messages.success(
            request,
            "Booking deleted successfully."
        )

        return super().delete(
            request,
            *args,
            **kwargs
        )


# =========================================================
# QUICK STATUS UPDATE
# =========================================================

class BookingStatusUpdateView(
    StaffRequiredMixin,
    UpdateView
):

    model = Booking

    fields = ["status"]

    pk_url_kwarg = "pk"


    def post(
        self,
        request,
        *args,
        **kwargs
    ):

        booking = self.get_object()

        new_status = request.POST.get(
            "status"
        )


        valid_statuses = dict(
            Booking.STATUS_CHOICES
        )


        if new_status not in valid_statuses:

            messages.error(
                request,
                "Invalid booking status."
            )

            return redirect(
                "booking_detail",
                pk=booking.pk
            )


        old_status = booking.status


        booking.status = new_status


        # =========================================
        # ADMIN CANCELLATION
        # =========================================

        if new_status == "cancelled":

            booking.cancelled_at = (
                timezone.now()
            )

            booking.cancelled_by = "admin"


            if booking.payment_status in [
                "paid",
                "partial",
            ]:

                booking.payment_status = "failed"


        # =========================================
        # SAVE
        # =========================================

        booking.save()


        # =========================================
        # SEND EMAIL
        # =========================================

        if old_status != new_status:

            try:

                booking.send_booking_email(
                    new_status
                )

            except Exception:

                pass


        messages.success(
            request,
            f"Booking status updated to {booking.get_status_display()}."
        )


        return redirect(
            "booking_detail",
            pk=booking.pk
        )
        
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from tourist.models import Tour, TourSchedule, TourPricing
from user.models import User


@require_GET
def booking_tour_options(request):

    tour_id = request.GET.get("tour_id")

    if not tour_id:
        return JsonResponse({
            "success": False,
            "message": "Tour is required.",
            "times": [],
            "guides": [],
            "pricing": [],
        })


    try:
        tour = Tour.objects.get(
            id=tour_id,
            is_active=True
        )

    except Tour.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Tour not found.",
            "times": [],
            "guides": [],
            "pricing": [],
        })


    # =========================================================
    # SCHEDULED TIMES
    # =========================================================

    schedules = (
        TourSchedule.objects
        .filter(
            tour=tour,
            is_active=True
        )
        .order_by("start_time")
    )


    times = []

    for schedule in schedules:

        times.append({
            # IMPORTANT:
            # This is the actual value submitted to Django.
            "value": schedule.start_time.strftime("%H:%M:%S"),

            # This is only what the user sees.
            "display": schedule.start_time.strftime("%I:%M %p"),

            "available_slots": schedule.available_slots,
        })


    # =========================================================
    # GUIDES
    # ONLY GUIDES FOR SELECTED TOUR LOCATION
    # =========================================================

    guides = []

    if tour.location_id:

        guide_queryset = (
            User.objects
            .filter(
                role="guide",
                is_active=True,
                locations=tour.location
            )
            .order_by("username")
            .distinct()
        )

        for guide in guide_queryset:

            guides.append({
                "id": guide.id,
                "name": (
                    guide.get_full_name()
                    or guide.username
                ),
            })


    # =========================================================
    # PRICING
    # =========================================================

    pricing_queryset = (
        TourPricing.objects
        .filter(
            tour=tour,
            is_active=True
        )
        .order_by("group_price")
    )


    pricing = []

    for price in pricing_queryset:

        pricing.append({
            "id": price.id,
            "label": price.get_group_type_display(),
            "price": str(price.group_price),
        })


    # =========================================================
    # LOCATION
    # =========================================================

    location = None

    if tour.location_id:
        location = str(tour.location)


    # =========================================================
    # RESPONSE
    # =========================================================

    return JsonResponse({
        "success": True,
        "times": times,
        "guides": guides,
        "pricing": pricing,
        "location": location,
    })
    
    
    


from tourist.models import FAQ
from .forms import FAQForm


class FAQListView(ListView):
    model = FAQ
    template_name = "tourist_admin/faq/list.html"
    context_object_name = "faqs"

    def get_queryset(self):
        queryset = FAQ.objects.all().order_by("order", "-created_at")

        search = self.request.GET.get("search", "").strip()

        if search:
            queryset = queryset.filter(
                question__icontains=search
            )

        return queryset


class FAQCreateView(CreateView):
    model = FAQ
    form_class = FAQForm
    template_name = "tourist_admin/faq/form.html"
    success_url = reverse_lazy("faq-list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "FAQ created successfully."
        )

        return super().form_valid(form)


class FAQUpdateView(UpdateView):
    model = FAQ
    form_class = FAQForm
    template_name = "tourist_admin/faq/form.html"
    success_url = reverse_lazy("faq-list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "FAQ updated successfully."
        )

        return super().form_valid(form)


class FAQDeleteView(DeleteView):
    model = FAQ
    success_url = reverse_lazy("faq-list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "FAQ deleted successfully."
        )
        return super().form_valid(form)
    
    
