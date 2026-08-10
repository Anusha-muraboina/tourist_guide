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


class TourScheduleForm(forms.ModelForm):
    class Meta:
        model = TourSchedule
        fields = "__all__"
        widgets = {
            "start_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
        }


class TourPricingForm(forms.ModelForm):
    class Meta:
        model = TourPricing
        fields = "__all__"
        
        
        

# from django import forms

# from tourist.models import (
#     Tour
# )


class TourForm(forms.ModelForm):

    class Meta:

        model = Tour

        fields = [
            "category",
            "title",
            "slug",
            "short_description",
            "full_description",
            "city",
            "state",
            "country",
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
        ]

        widgets = {

            "short_description": forms.Textarea(
                attrs={
                    "rows": 3
                }
            ),

            "full_description": forms.Textarea(
                attrs={
                    "rows": 6
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "rows": 3
                }
            ),

            "meeting_point": forms.Textarea(
                attrs={
                    "rows": 3
                }
            ),

            "includes": forms.SelectMultiple(
                attrs={
                    "class": "form-control"
                }
            ),

            "excludes": forms.SelectMultiple(
                attrs={
                    "class": "form-control"
                }
            ),

            "highlights": forms.SelectMultiple(
                attrs={
                    "class": "form-control"
                }
            ),

            "important_information": forms.SelectMultiple(
                attrs={
                    "class": "form-control"
                }
            ),

            "amenities": forms.SelectMultiple(
                attrs={
                    "class": "form-control"
                }
            ),

        }
        
        



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


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"
        
        


from django import forms
from blog.models import Blog


class BlogForm(forms.ModelForm):

    class Meta:

        model = Blog

        fields = "__all__"

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            if field.widget.__class__.__name__ != "CKEditorWidget":

                field.widget.attrs.update({
                    "class": "w-full border rounded-lg px-4 py-2"
                })
                
                
                

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
                
                
                
from django import forms
from booking.models import Booking
from tourist.models import Tour
from user.models import User


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = [
            "tour",
            "guide",
            "guest_name",
            "guest_email",
            "guest_phone",
            "adults",
            "children",
            "infants",
            "tour_date",
            "tour_time",
            "special_requests",
            "payment_method",
            "payment_status",
            "status",
        ]
        widgets = {
            "tour": forms.Select(attrs={"class": "form-control"}),
            "guide": forms.Select(attrs={"class": "form-control"}),
            "guest_name": forms.TextInput(attrs={"class": "form-control"}),
            "guest_email": forms.EmailInput(attrs={"class": "form-control"}),
            "guest_phone": forms.TextInput(attrs={"class": "form-control"}),
            "adults": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "children": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "infants": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "tour_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "tour_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "special_requests": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "payment_method": forms.Select(attrs={"class": "form-control"}),
            "payment_status": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only show active guides
        self.fields["guide"].queryset = User.objects.filter(
            role="guide",
            is_active=True
        )

        # Only show active tours
        self.fields["tour"].queryset = Tour.objects.filter(is_active=True)
