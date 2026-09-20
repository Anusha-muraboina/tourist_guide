from django import forms
from tourist.models import (
    TourCategory,
    TourHighlight,
    TourInclude,
    TourExclude,
    ImportantInformation,
    Amenity,
    Tour
)


class TourCategoryForm(forms.ModelForm):
    class Meta:
        model = TourCategory
        fields = "__all__"


class TourHighlightForm(forms.ModelForm):
    class Meta:
        model = TourHighlight
        fields = "__all__"


class TourIncludeForm(forms.ModelForm):
    class Meta:
        model = TourInclude
        fields = "__all__"


class TourExcludeForm(forms.ModelForm):
    class Meta:
        model = TourExclude
        fields = "__all__"


class ImportantInformationForm(forms.ModelForm):
    class Meta:
        model = ImportantInformation
        fields = "__all__"


class AmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        fields = "__all__"
        
        

# from django import forms
from tourist.models import TourSchedule, TourPricing


# class TourScheduleForm(forms.ModelForm):
#     class Meta:
#         model = TourSchedule
#         fields = "__all__"
#         widgets = {
#             "start_time": forms.TimeInput(
#                 attrs={"type": "time"}
#             ),
#         }
        

class TourScheduleForm(forms.ModelForm):
    class Meta:
        model = TourSchedule
        fields = "__all__"

        widgets = {
            "start_time": forms.TimeInput(
                format="%H:%M",
                attrs={
                    "type": "time",
                    "step": "60",  # 1-minute intervals
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["start_time"].input_formats = [
            "%H:%M",
            "%H:%M:%S",
        ]
        
        
           
# class TourPricingForm(forms.ModelForm):
#     class Meta:
#         model = TourPricing
#         fields = "__all__"
        
    
    


class TourPricingForm(forms.ModelForm):
    class Meta:
        model = TourPricing
        fields = [
            "tour",
            "group_type",
            "group_members",
            "group_price",
            "is_active",
        ]

        widgets = {
            "tour": forms.Select(attrs={
                "class": "w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 text-sm focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none",
            }),

            "group_type": forms.Select(attrs={
                "class": "w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 text-sm focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none",
            }),

            "group_members": forms.TextInput(attrs={
                "class": "w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 text-sm focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none",
                "placeholder": "Example: 5 members",
            }),

            "group_price": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 text-sm focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none",
                "placeholder": "Enter group price",
                "step": "0.01",
                "min": "0",
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "h-5 w-5 text-blue-600 rounded border-slate-300 focus:ring-blue-500 cursor-pointer",
            }),
        }

        labels = {
            "tour": "Tour",
            "group_type": "Group Type",
            "group_members": "Group Members",
            "group_price": "Group Price",
            "is_active": "Active Status",
        }    
        

# from django import forms

# from tourist.models import (
#     Tour
# )


# class TourForm(forms.ModelForm):

#     class Meta:

#         model = Tour

#         fields = [
#             "category",
#             "title",
#             "slug",
#             "short_description",
#             "full_description",
#             # "city",
#             # "state",
#             # "country",
#             "address",
#             "meeting_point",
#             "duration",
#             "language",
#             "tour_type",
#             "max_people",
#             "min_age",
#             "free_cancellation",
#             "instant_confirmation",
#             "pickup_available",
#             "wheelchair_accessible",
#             "featured",
#             "slot_position",
#             "includes",
#             "excludes",
#             "highlights",
#             "important_information",
#             "amenities",
#             "is_active",
            
#             "seo_title",
#             "seo_description",
#             "seo_keywords",
#         ]

#         widgets = {

#             "short_description": forms.Textarea(
#                 attrs={
#                     "rows": 3
#                 }
#             ),

#             "full_description": forms.Textarea(
#                 attrs={
#                     "rows": 6
#                 }
#             ),

#             "address": forms.Textarea(
#                 attrs={
#                     "rows": 3
#                 }
#             ),

#             "meeting_point": forms.Textarea(
#                 attrs={
#                     "rows": 3
#                 }
#             ),

#             "includes": forms.SelectMultiple(
#                 attrs={
#                     "class": "form-control"
#                 }
#             ),
#             "excludes": forms.SelectMultiple(
#                 attrs={
#                     "class": "form-control"
#                 }
#             ),
#             "highlights": forms.SelectMultiple(
#                 attrs={
#                     "class": "form-control"
#                 }
#             ),
#             "important_information": forms.SelectMultiple(
#                 attrs={
#                     "class": "form-control"
#                 }
#             ),

#             "amenities": forms.SelectMultiple(
#                 attrs={
#                     "class": "form-control"
#                 }
#             ),

#         }
        
        
from django import forms

from tourist.models import (
    Tour,
    TourInclude,
    TourExclude,
    TourHighlight,
    ImportantInformation,
    Amenity,
)




# class TourForm(forms.ModelForm):

#     class Meta:

#         model = Tour

#         fields = [
#             "category",
#             "title",
#             "slug",
#             "short_description",
#             "full_description",

#             # LOCATION
#             "location",
#             "address",
#             "meeting_point",

#             "duration",
#             "language",
#             "tour_type",
#             "max_people",
#             "min_age",

#             "free_cancellation",
#             "instant_confirmation",
#             "pickup_available",
#             "wheelchair_accessible",
#             "featured",
#             "slot_position",

#             "includes",
#             "excludes",
#             "highlights",
#             "important_information",
#             "amenities",

#             "is_active",

#             "seo_title",
#             "seo_description",
#             "seo_keywords",
#         ]

#         widgets = {

#             # ==========================================
#             # LOCATION
#             # ==========================================

#             "location": forms.Select(
#                 attrs={
#                     "class": "location-input",
#                     "data-placeholder": "Choose a tour location"
#                 }
#             ),

#             # ==========================================
#             # TEXT AREAS
#             # ==========================================

#             "short_description": forms.Textarea(
#                 attrs={
#                     "rows": 4,
#                     "placeholder":
#                         "Write a short description..."
#                 }
#             ),

#             "full_description": forms.Textarea(
#                 attrs={
#                     "rows": 7,
#                     "placeholder":
#                         "Write the complete tour description..."
#                 }
#             ),

#             "address": forms.Textarea(
#                 attrs={
#                     "rows": 3,
#                     "placeholder":
#                         "Enter the complete tour address..."
#                 }
#             ),

#             "meeting_point": forms.Textarea(
#                 attrs={
#                     "rows": 3,
#                     "placeholder":
#                         "Example: Main entrance of Charminar..."
#                 }
#             ),

#             # ==========================================
#             # MANY TO MANY
#             # ==========================================

#             "includes": forms.CheckboxSelectMultiple(),

#             "excludes": forms.CheckboxSelectMultiple(),

#             "highlights": forms.CheckboxSelectMultiple(),

#             "important_information":
#                 forms.CheckboxSelectMultiple(),

#             "amenities":
#                 forms.CheckboxSelectMultiple(),
#         }


#     def __init__(self, *args, **kwargs):

#         super().__init__(*args, **kwargs)

#         # ==============================================
#         # ACTIVE LOCATIONS ONLY
#         # ==============================================

#         self.fields["location"].queryset = (
#             Location.objects
#             .filter(is_active=True)
#             .order_by(
#                 "state",
#                 "district",
#                 "city"
#             )
#         )

#         # ==============================================
#         # CATEGORY
#         # ==============================================

#         self.fields["category"].queryset = (
#             TourCategory.objects
#             .filter(is_active=True)
#             .order_by(
#                 "slot_position",
#                 "name"
#             )
#         )

#         # ==============================================
#         # M2M
#         # ==============================================

#         self.fields["includes"].queryset = (
#             TourInclude.objects
#             .filter(is_active=True)
#             .order_by(
#                 "slot_position",
#                 "title"
#             )
#         )

#         self.fields["excludes"].queryset = (
#             TourExclude.objects
#             .filter(is_active=True)
#             .order_by(
#                 "slot_position",
#                 "title"
#             )
#         )

#         self.fields["highlights"].queryset = (
#             TourHighlight.objects
#             .filter(is_active=True)
#             .order_by(
#                 "slot_position",
#                 "title"
#             )
#         )

#         self.fields["important_information"].queryset = (
#             ImportantInformation.objects
#             .filter(is_active=True)
#             .order_by(
#                 "slot_position",
#                 "title"
#             )
#         )

#         self.fields["amenities"].queryset = (
#             Amenity.objects
#             .filter(is_active=True)
#             .order_by(
#                 "slot_position",
#                 "name"
#             )
#         )


from django import forms

from tourist.models import (
    Tour,
    TourCategory,
    TourInclude,
    TourExclude,
    TourHighlight,
    ImportantInformation,
    Amenity,
)

from user.models import Location


# ============================================================
# TOUR FORM
# ============================================================
from django import forms

from tourist.models import (
    Tour,
    TourCategory,
    TourInclude,
    TourExclude,
    TourHighlight,
    ImportantInformation,
    Amenity,
)

from user.models import Location


# ============================================================
# TOUR FORM
# ============================================================

class TourForm(forms.ModelForm):

    class Meta:

        model = Tour

        fields = [
            "category",
            "title",
            "slug",

            "short_description",
            "full_description",

            "location",
            "address",
            "meeting_point",

            "duration",
            "language",
            "tour_type",

            "max_people",
            "min_age",

            "free_cancellation",
            "instant_confirmation",
            "pickup_available",
            "wheelchair_accessible",

            "featured",
            "slot_position",

            "includes",
            "excludes",
            "highlights",
            "important_information",
            "amenities",

            "is_active",

            "seo_title",
            "seo_description",
            "seo_keywords",
        ]

        widgets = {

            # ------------------------------------------------
            # LOCATION
            # ------------------------------------------------

            "location": forms.Select(
                attrs={
                    "class": "location-input",
                    "data-placeholder":
                        "Choose a tour location",
                }
            ),

            # ------------------------------------------------
            # TEXT AREAS
            # ------------------------------------------------

            "short_description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder":
                        "Write a short description...",
                }
            ),

            "full_description": forms.Textarea(
                attrs={
                    "rows": 7,
                    "placeholder":
                        "Write the complete tour description...",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder":
                        "Enter the complete tour address...",
                }
            ),

            "meeting_point": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder":
                        "Example: Main entrance of Charminar...",
                }
            ),

            # ------------------------------------------------
            # MANY TO MANY
            # ------------------------------------------------

            "includes":
                forms.CheckboxSelectMultiple(),

            "excludes":
                forms.CheckboxSelectMultiple(),

            "highlights":
                forms.CheckboxSelectMultiple(),

            "important_information":
                forms.CheckboxSelectMultiple(),

            "amenities":
                forms.CheckboxSelectMultiple(),
        }

    # ========================================================
    # INIT
    # ========================================================

    def __init__(
        self,
        *args,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )

        # ----------------------------------------------------
        # ACTIVE LOCATIONS
        # ----------------------------------------------------

        self.fields[
            "location"
        ].queryset = (
            Location.objects
            .filter(
                is_active=True
            )
            .order_by(
                "state",
                "district",
                "city",
            )
        )

        # ----------------------------------------------------
        # ACTIVE CATEGORIES
        # ----------------------------------------------------

        self.fields[
            "category"
        ].queryset = (
            TourCategory.objects
            .filter(
                is_active=True
            )
            .order_by(
                "slot_position",
                "name",
            )
        )

        # ----------------------------------------------------
        # INCLUDES
        # ----------------------------------------------------

        self.fields[
            "includes"
        ].queryset = (
            TourInclude.objects
            .filter(
                is_active=True
            )
            .order_by(
                "slot_position",
                "title",
            )
        )

        # ----------------------------------------------------
        # EXCLUDES
        # ----------------------------------------------------

        self.fields[
            "excludes"
        ].queryset = (
            TourExclude.objects
            .filter(
                is_active=True
            )
            .order_by(
                "slot_position",
                "title",
            )
        )

        # ----------------------------------------------------
        # HIGHLIGHTS
        # ----------------------------------------------------

        self.fields[
            "highlights"
        ].queryset = (
            TourHighlight.objects
            .filter(
                is_active=True
            )
            .order_by(
                "slot_position",
                "title",
            )
        )

        # ----------------------------------------------------
        # IMPORTANT INFORMATION
        # ----------------------------------------------------

        self.fields[
            "important_information"
        ].queryset = (
            ImportantInformation.objects
            .filter(
                is_active=True
            )
            .order_by(
                "slot_position",
                "title",
            )
        )

        # ----------------------------------------------------
        # AMENITIES
        # ----------------------------------------------------

        self.fields[
            "amenities"
        ].queryset = (
            Amenity.objects
            .filter(
                is_active=True
            )
            .order_by(
                "slot_position",
                "name",
            )
        )


from django import forms

from contact.models import ContactUs


# class ContactUsForm(forms.ModelForm):

#     class Meta:
#         model = ContactUs
#         fields = [
#             "name",
#             "email",
#             "phone_number",
#             "message",
#             "is_read",
#         ]

#         widgets = {

#             "name": forms.TextInput(attrs={
#                 "class": "form-control"
#             }),

#             "email": forms.EmailInput(attrs={
#                 "class": "form-control"
#             }),

#             "phone_number": forms.TextInput(attrs={
#                 "class": "form-control"
#             }),

#             "message": forms.Textarea(attrs={
#                 "rows": 5,
#                 "class": "form-control"
#             }),

#             "is_read": forms.CheckboxInput(attrs={
#                 "class": "form-check-input"
#             }),

#         }



from django import forms

from contact.models import ContactUs


class ContactUsForm(forms.ModelForm):

    class Meta:
        model = ContactUs
        fields = [
            "name",
            "email",
            "phone_number",
            "message",
            "is_read",
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Text Input Style
        input_class = (
            "w-full rounded-xl border border-gray-300 "
            "px-4 py-3 text-gray-700 placeholder-gray-400 "
            "focus:outline-none focus:ring-2 "
            "focus:ring-teal-500 focus:border-teal-500 "
            "transition duration-200"
        )

        # Textarea Style
        textarea_class = (
            "w-full rounded-xl border border-gray-300 "
            "px-4 py-3 text-gray-700 placeholder-gray-400 "
            "focus:outline-none focus:ring-2 "
            "focus:ring-teal-500 focus:border-teal-500 "
            "transition duration-200 resize-none"
        )

        # Checkbox Style
        checkbox_class = (
            "h-5 w-5 rounded border-gray-300 "
            "text-teal-600 focus:ring-teal-500"
        )

        self.fields["name"].widget.attrs.update({
            "class": input_class,
            "placeholder": "Enter full name",
        })

        self.fields["email"].widget.attrs.update({
            "class": input_class,
            "placeholder": "Enter email address",
        })

        self.fields["phone_number"].widget.attrs.update({
            "class": input_class,
            "placeholder": "Enter phone number",
        })

        self.fields["message"].widget = forms.Textarea(
            attrs={
                "class": textarea_class,
                "rows": 6,
                "placeholder": "Type customer message...",
            }
        )


        self.fields["is_read"].widget.attrs.update({
            "class": checkbox_class,
        })

        # Friendly Labels
        self.fields["name"].label = "Full Name"
        self.fields["email"].label = "Email Address"
        self.fields["phone_number"].label = "Phone Number"
        self.fields["message"].label = "Message"
        self.fields["is_read"].label = "Mark as Read"

        # Optional Help Text
        self.fields["is_read"].help_text = (
            "Enable this if you have reviewed this enquiry."
        )
        
        

from django import forms

from coupon.models import Coupon


class CouponForm(forms.ModelForm):

    class Meta:
        model = Coupon
        exclude = [
            "used_count",
            "created_at",
        ]

        widgets = {

            "title": forms.TextInput(),

            "code": forms.TextInput(),

            "tour": forms.Select(),

            "discount_type": forms.Select(),

            "discount_value": forms.NumberInput(),

            "min_booking_amount": forms.NumberInput(),

            "max_discount_amount": forms.NumberInput(),

            "start_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "end_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "usage_limit": forms.NumberInput(),

            "is_active": forms.CheckboxInput(),

        }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        input_class = (
            "w-full rounded-xl border border-gray-300 "
            "px-4 py-3 "
            "focus:outline-none "
            "focus:ring-2 "
            "focus:ring-teal-500 "
            "focus:border-teal-500"
        )

        select_class = (
            "w-full rounded-xl border border-gray-300 "
            "px-4 py-3 bg-white "
            "focus:outline-none "
            "focus:ring-2 "
            "focus:ring-teal-500"
        )

        checkbox_class = (
            "w-5 h-5 text-teal-600 rounded border-gray-300"
        )

        for name, field in self.fields.items():

            if isinstance(field.widget, forms.Select):

                field.widget.attrs.update({
                    "class": select_class
                })

            elif isinstance(field.widget, forms.CheckboxInput):

                field.widget.attrs.update({
                    "class": checkbox_class
                })

            else:

                field.widget.attrs.update({
                    "class": input_class
                })


        self.fields["title"].widget.attrs["placeholder"] = "Summer Offer"

        self.fields["code"].widget.attrs["placeholder"] = "SUMMER50"

        self.fields["discount_value"].widget.attrs["placeholder"] = "10 or 500"

        self.fields["min_booking_amount"].widget.attrs["placeholder"] = "1000"

        self.fields["max_discount_amount"].widget.attrs["placeholder"] = "1000"

        self.fields["usage_limit"].widget.attrs["placeholder"] = "0 = Unlimited"

        self.fields["title"].label = "Coupon Title"

        self.fields["code"].label = "Coupon Code"

        self.fields["tour"].empty_label = "All Tours"
        
        
        
        


from django import forms

from rating.models import (
    Rating,
    RatingImage
)


class RatingForm(forms.ModelForm):

    class Meta:

        model = Rating

        fields = [
            "user",
            "tour",
            "rating",
            "review",
            "anonymous",
            "active",
        ]

        widgets = {

            "user": forms.Select(attrs={
                "class": "w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
            }),

            "tour": forms.Select(attrs={
                "class": "w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
            }),

            "rating": forms.NumberInput(attrs={
                "step": "0.5",
                "min": "1",
                "max": "5",
                "placeholder": "Example: 4.5",
                "class": "w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
            }),

            "review": forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "Write customer review...",
                "class": "w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 resize-none"
            }),

            "anonymous": forms.CheckboxInput(attrs={
                "class": "h-5 w-5 rounded text-teal-600 border-gray-300"
            }),

            "active": forms.CheckboxInput(attrs={
                "class": "h-5 w-5 rounded text-teal-600 border-gray-300"
            }),

        }
        
        
        
from django import forms
from blog.models import Blog, BlogCategory


class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = "__all__"


# class BlogForm(forms.ModelForm):
#     class Meta:
#         model = Blog
#         fields = "__all__"
        
        


from django import forms
from blog.models import Blog


# class BlogForm(forms.ModelForm):

#     class Meta:

#         model = Blog

#         fields = "__all__"

#     def __init__(self, *args, **kwargs):

#         super().__init__(*args, **kwargs)

#         for field in self.fields.values():

#             if field.widget.__class__.__name__ != "CKEditorWidget":

#                 field.widget.attrs.update({
#                     "class": "w-full border rounded-lg px-4 py-2"
#                 })
                
     
from django import forms

from blog.models import Blog, BlogCategory

from ckeditor.widgets import CKEditorWidget


# class BlogCategoryForm(forms.ModelForm):

#     class Meta:

#         model = BlogCategory

#         fields = [
#             "name",
#             "slug",
#             "is_active",
#             "slot_position",
#         ]


class BlogForm(forms.ModelForm):

    description = forms.CharField(
        widget=CKEditorWidget(
            config_name="default"
        )
    )

    class Meta:

        model = Blog

        fields = [
            "category",
            "title",
            "slug",
            "short_description",
            "description",
            "image",
            "author",
            "reading_time",
            "featured",
            "is_active",
            "slot_position",
            "meta_title",
            "meta_description",
            "meta_keywords",
        ]

        widgets = {

            "category": forms.Select(
                attrs={
                    "class": (
                        "w-full border border-slate-300 "
                        "rounded-xl px-4 py-3 "
                        "focus:ring-2 focus:ring-cyan-500 "
                        "focus:border-cyan-500 outline-none"
                    )
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": (
                        "w-full border border-slate-300 "
                        "rounded-xl px-4 py-3 "
                        "focus:ring-2 focus:ring-cyan-500 "
                        "focus:border-cyan-500 outline-none"
                    ),
                    "placeholder": "Enter blog title"
                }
            ),

            "slug": forms.TextInput(
                attrs={
                    "class": (
                        "w-full border border-slate-300 "
                        "rounded-xl px-4 py-3 "
                        "focus:ring-2 focus:ring-cyan-500 "
                        "focus:border-cyan-500 outline-none"
                    ),
                    "placeholder": "blog-url-slug"
                }
            ),

            "short_description": forms.Textarea(
                attrs={
                    "class": (
                        "w-full border border-slate-300 "
                        "rounded-xl px-4 py-3 "
                        "focus:ring-2 focus:ring-cyan-500 "
                        "focus:border-cyan-500 outline-none"
                    ),
                    "rows": 4,
                    "placeholder": "Enter short description"
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": (
                        "w-full border border-slate-300 "
                        "rounded-xl px-4 py-3 bg-white"
                    ),
                    "accept": "image/*"
                }
            ),

            "author": forms.TextInput(
                attrs={
                    "class": (
                        "w-full border border-slate-300 "
                        "rounded-xl px-4 py-3 "
                        "focus:ring-2 focus:ring-cyan-500 "
                        "focus:border-cyan-500 outline-none"
                    ),
                    "placeholder": "Author name"
                }
            ),

            "reading_time": forms.NumberInput(
                attrs={
                    "class": (
                        "w-full border border-slate-300 "
                        "rounded-xl px-4 py-3 "
                        "focus:ring-2 focus:ring-cyan-500 "
                        "focus:border-cyan-500 outline-none"
                    ),
                    "min": 1
                }
            ),

            "slot_position": forms.NumberInput(
                attrs={
                    "class": (
                        "w-full border border-slate-300 "
                        "rounded-xl px-4 py-3 "
                        "focus:ring-2 focus:ring-cyan-500 "
                        "focus:border-cyan-500 outline-none"
                    ),
                    "min": 0
                }
            ),

            "meta_title": forms.TextInput(
                attrs={
                    "class": (
                        "w-full border border-slate-300 "
                        "rounded-xl px-4 py-3 "
                        "focus:ring-2 focus:ring-cyan-500 "
                        "focus:border-cyan-500 outline-none"
                    ),
                    "maxlength": 255,
                    "placeholder": "SEO title"
                }
            ),

            "meta_description": forms.Textarea(
                attrs={
                    "class": (
                        "w-full border border-slate-300 "
                        "rounded-xl px-4 py-3 "
                        "focus:ring-2 focus:ring-cyan-500 "
                        "focus:border-cyan-500 outline-none"
                    ),
                    "rows": 4,
                    "maxlength": 160,
                    "placeholder": "SEO description"
                }
            ),

            "meta_keywords": forms.Textarea(
                attrs={
                    "class": (
                        "w-full border border-slate-300 "
                        "rounded-xl px-4 py-3 "
                        "focus:ring-2 focus:ring-cyan-500 "
                        "focus:border-cyan-500 outline-none"
                    ),
                    "rows": 3,
                    "placeholder": "travel, hyderabad, tourism, tours"
                }
            ),

            "featured": forms.CheckboxInput(
                attrs={
                    "class": "w-5 h-5 text-cyan-600"
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "w-5 h-5 text-cyan-600"
                }
            ),
        }    
                

from booking.models import CancelReason ,BookingCancelComment


class CancelReasonForm(forms.ModelForm):

    class Meta:

        model = CancelReason

        fields = "__all__"

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({

                "class": "w-full rounded-lg border border-gray-300 px-4 py-2 focus:ring-2 focus:ring-blue-500"

            })
            
            
            



class BookingCancelCommentForm(forms.ModelForm):

    class Meta:

        model = BookingCancelComment

        fields = "__all__"

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({

                "class": "w-full border border-gray-300 rounded-lg px-4 py-2"

            })

        self.fields["comment"].widget.attrs["rows"] = 5
        
        

# from django import forms
from booking.models import TourPaymentPolicy


class TourPaymentPolicyForm(forms.ModelForm):

    class Meta:
        model = TourPaymentPolicy
        fields = "__all__"

        widgets = {
            "tour": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
            "allow_pay_at_location": forms.CheckboxInput(
                attrs={
                    "class": "h-5 w-5"
                }
            ),
            "allow_partial_payment": forms.CheckboxInput(
                attrs={
                    "class": "h-5 w-5"
                }
            ),
            "allow_full_payment": forms.CheckboxInput(
                attrs={
                    "class": "h-5 w-5"
                }
            ),
        }
        
        
        
from django import forms
from user.models import Location


class LocationForm(forms.ModelForm):

    class Meta:

        model = Location

        fields = [
            "country",
            "state",
            "district",
            "city",
            "is_active",
        ]
        
        

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "phone_number",
            "role",
            "locations",
            "profile_image",
            "is_verified",
            "is_active",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():

            if name == "locations":
                field.widget.attrs.update({
                    "class": "w-full rounded-xl border border-slate-300 p-3 h-64"
                })

            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    "class": "w-5 h-5 rounded text-indigo-600"
                })

            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({
                    "class": "block w-full text-sm border rounded-xl p-2"
                })

            else:
                field.widget.attrs.update({
                    "class": "w-full rounded-xl border border-slate-300 px-4 py-3 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                })
                
                
                

from booking.models import Booking
from user.models import User


from tourist.models import Tour, TourPricing
from django import forms
from django.utils import timezone

from booking.models import Booking
from tourist.models import Tour, TourSchedule, TourPricing
from user.models import User
from django import forms
from django.utils import timezone

from booking.models import Booking
from tourist.models import Tour, TourSchedule, TourPricing
from user.models import User

from decimal import Decimal

from django import forms
from django.utils import timezone

from booking.models import Booking
from tourist.models import Tour, TourSchedule, TourPricing
from user.models import User


class BookingForm(forms.ModelForm):

    # =========================================================
    # TOUR TIME
    # Booking.tour_time is a TimeField
    # =========================================================

    tour_time = forms.ChoiceField(
        required=True,
        choices=[
            ("", "Select scheduled time")
        ],
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "id_tour_time",
            }
        ),
    )


    class Meta:

        model = Booking

        fields = [
            "tour",
            "tour_date",
            "tour_time",
            "pricing",
            "group_members",
            "guide",
            "guest_name",
            "guest_email",
            "guest_phone",
            "payment_method",
            "payment_status",
            "status",
            "special_requests",
        ]

        widgets = {

            "tour": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "id_tour",
                }
            ),

            "tour_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "id": "id_tour_date",
                    "type": "date",
                }
            ),

            "pricing": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "id_pricing",
                }
            ),

            "group_members": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "id_group_members",
                    "min": "1",
                }
            ),

            "guide": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "id_guide",
                }
            ),

            "guest_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Guest name",
                }
            ),

            "guest_email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Guest email",
                }
            ),

            "guest_phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Guest phone number",
                }
            ),

            "payment_method": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "payment_status": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "special_requests": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Any special requests...",
                }
            ),
        }


    # =========================================================
    # INIT
    # =========================================================

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        # =====================================================
        # TOUR
        # =====================================================

        self.fields["tour"].queryset = (
            Tour.objects
            .filter(is_active=True)
            .order_by("title")
        )


        # =====================================================
        # EMPTY DEPENDENT FIELDS
        # =====================================================

        self.fields["tour_time"].choices = [
            ("", "Select scheduled time")
        ]

        self.fields["guide"].queryset = (
            User.objects.none()
        )

        self.fields["pricing"].queryset = (
            TourPricing.objects.none()
        )


        # =====================================================
        # GET SELECTED TOUR
        # =====================================================

        selected_tour_id = None


        # -----------------------------------------------------
        # EDIT
        # -----------------------------------------------------

        if (
            self.instance
            and self.instance.pk
        ):

            selected_tour_id = (
                self.instance.tour_id
            )


        # -----------------------------------------------------
        # CREATE / POST
        # -----------------------------------------------------

        if self.is_bound:

            selected_tour_id = (
                self.data.get("tour")
                or selected_tour_id
            )


        # =====================================================
        # LOAD TOUR DATA
        # =====================================================

        if selected_tour_id:

            try:

                tour = Tour.objects.get(
                    id=selected_tour_id,
                    is_active=True
                )

            except Tour.DoesNotExist:

                tour = None


            if tour:

                # =============================================
                # SCHEDULES
                # =============================================

                schedules = (
                    TourSchedule.objects
                    .filter(
                        tour=tour,
                        is_active=True
                    )
                    .order_by("start_time")
                )


                self.fields["tour_time"].choices = [

                    (
                        "",
                        "Select scheduled time"
                    )

                ] + [

                    (
                        schedule.start_time.strftime(
                            "%H:%M:%S"
                        ),

                        schedule.start_time.strftime(
                            "%I:%M %p"
                        )

                    )

                    for schedule in schedules

                ]


                # =============================================
                # PRICING
                # =============================================

                self.fields["pricing"].queryset = (
                    TourPricing.objects
                    .filter(
                        tour=tour,
                        is_active=True
                    )
                    .order_by("group_price")
                )


                # =============================================
                # GUIDES
                # =============================================

                if tour.location_id:

                    self.fields["guide"].queryset = (
                        User.objects
                        .filter(
                            role="guide",
                            is_active=True,
                            locations=tour.location
                        )
                        .order_by("username")
                        .distinct()
                    )


    # =========================================================
    # VALIDATION
    # =========================================================

    def clean(self):

        cleaned_data = super().clean()

        tour = cleaned_data.get("tour")
        tour_time = cleaned_data.get("tour_time")
        pricing = cleaned_data.get("pricing")
        guide = cleaned_data.get("guide")
        tour_date = cleaned_data.get("tour_date")
        group_members = cleaned_data.get("group_members")


        if not tour:

            return cleaned_data


        # =====================================================
        # TIME VALIDATION
        # =====================================================

        if tour_time:

            valid_time = (
                TourSchedule.objects
                .filter(
                    tour=tour,
                    start_time=tour_time,
                    is_active=True
                )
                .exists()
            )


            if not valid_time:

                self.add_error(
                    "tour_time",
                    "Selected time is not available for this tour."
                )


        # =====================================================
        # PRICING VALIDATION
        # =====================================================

        if pricing:

            if pricing.tour_id != tour.id:

                self.add_error(
                    "pricing",
                    "Selected pricing does not belong to this tour."
                )


        # =====================================================
        # GUIDE VALIDATION
        # =====================================================

        if guide:

            if not tour.location_id:

                self.add_error(
                    "guide",
                    "This tour does not have a location."
                )

            elif not guide.locations.filter(
                id=tour.location_id
            ).exists():

                self.add_error(
                    "guide",
                    "This guide is not available for the selected tour location."
                )


        # =====================================================
        # GROUP MEMBERS
        # =====================================================

        if group_members is not None:

            if group_members < 1:

                self.add_error(
                    "group_members",
                    "Group members must be at least 1."
                )


        # =====================================================
        # DATE
        # =====================================================

        if tour_date:

            if tour_date < timezone.localdate():

                self.add_error(
                    "tour_date",
                    "Tour date cannot be in the past."
                )


        return cleaned_data


    # =========================================================
    # SAVE BOOKING
    # =========================================================

    def save(self, commit=True):

        booking = super().save(commit=False)


        # =====================================================
        # SELECTED PRICING
        # =====================================================

        pricing = self.cleaned_data.get(
            "pricing"
        )


        # =====================================================
        # CALCULATE SUBTOTAL
        # =====================================================

        if pricing:

            sub_total = Decimal(
                str(pricing.group_price)
            )

        else:

            sub_total = Decimal(
                "0.00"
            )


        # =====================================================
        # DISCOUNT
        # =====================================================
        # Admin form currently has no coupon field,
        # so discount is zero.
        # =====================================================

        discount_amount = Decimal(
            "0.00"
        )


        # =====================================================
        # TAX
        # =====================================================
        # Current booking flow uses zero tax.
        # =====================================================

        tax_amount = Decimal(
            "0.00"
        )


        # =====================================================
        # TOTAL
        # =====================================================

        total_amount = (
            sub_total
            - discount_amount
            + tax_amount
        )


        # =====================================================
        # SAVE CALCULATED VALUES
        # =====================================================

        booking.sub_total = sub_total

        booking.discount_amount = (
            discount_amount
        )

        booking.tax_amount = (
            tax_amount
        )

        booking.total_amount = (
            total_amount
        )


        # =====================================================
        # PAYMENT DEFAULT
        # =====================================================

        if not booking.payment_status:

            booking.payment_status = (
                "pending"
            )


        # =====================================================
        # SAVE
        # =====================================================

        if commit:

            booking.save()

            self.save_m2m()


        return booking
    
    
    



from django import forms
from tourist.models import FAQ


class FAQForm(forms.ModelForm):

    class Meta:
        model = FAQ
        fields = [
            "question",
            "answer",
            "order",
            "is_active",
        ]

        widgets = {
            "question": forms.TextInput(
                attrs={
                    "class": (
                        "w-full px-4 py-3 rounded-xl border border-gray-300 "
                        "focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 "
                        "outline-none transition"
                    ),
                    "placeholder": "Enter FAQ question",
                }
            ),

            "answer": forms.Textarea(
                attrs={
                    "class": (
                        "w-full px-4 py-3 rounded-xl border border-gray-300 "
                        "focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 "
                        "outline-none transition resize-none"
                    ),
                    "rows": 6,
                    "placeholder": "Enter FAQ answer",
                }
            ),

            "order": forms.NumberInput(
                attrs={
                    "class": (
                        "w-full px-4 py-3 rounded-xl border border-gray-300 "
                        "focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 "
                        "outline-none transition"
                    ),
                    "min": 0,
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": (
                        "w-5 h-5 rounded border-gray-300 "
                        "text-indigo-600 focus:ring-indigo-500"
                    ),
                }
            ),
        }

        labels = {
            "question": "Question",
            "answer": "Answer",
            "order": "Display Order",
            "is_active": "Active",
        }