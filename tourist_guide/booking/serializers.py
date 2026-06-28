# # bookings/serializers.py

# from decimal import Decimal

# from rest_framework import serializers

# from booking.models import Booking

# from tourist.models import (
#  Tour, TourSchedule
# )

# from user.models import User
from coupon.models import Coupon ,CouponUsage

# bookings/serializers.py

from decimal import Decimal
from datetime import datetime

from rest_framework import serializers

from booking.models import Booking

from tourist.models import (
    Tour,
    TourSchedule,
    TourPricing
)

from user.models import User


# =====================================
# GUIDE SERIALIZER
# =====================================

class GuideSerializer(
    serializers.ModelSerializer
):
    profile_image = serializers.SerializerMethodField()

    class Meta:

        model = User

        fields = [

            "id",

            "username",

            "email",

            "phone_number",

            "location",
             "state",

            "profile_image"
        ]
    def get_profile_image(self, obj):

        request = self.context.get("request")

        if obj.profile_image and request:

            return request.build_absolute_uri(
                obj.profile_image.url
            )

        return None

# =====================================
# TOUR PRICING SERIALIZER
# =====================================

class TourPricingSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = TourPricing

        fields = [

            "person_type",

            "price"
        ]


# =====================================
# TOUR SERIALIZER
# =====================================

class TourSerializer(
    serializers.ModelSerializer
):

    pricing = TourPricingSerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Tour

        fields = [

            "id",

            "title",

            "slug",

            "city",

            "state",

            "country",

            "duration",

            "pricing"
        ]


# =====================================
# BOOKING SERIALIZER
# =====================================

class BookingCreateSerializer(
    serializers.ModelSerializer
):

    # =================================
    # OPTIONAL GUIDE
    # =================================

    guide = serializers.PrimaryKeyRelatedField(

        queryset=User.objects.filter(
            role="guide",
            is_active=True
        ),

        required=False,

        allow_null=True
    )
    
    coupon_code = serializers.CharField(
        required=False,
        allow_blank=True
    )

    # =================================
    # EXTRA FIELDS
    # =================================

    tour_details = serializers.SerializerMethodField()

    selected_guide = serializers.SerializerMethodField()

    matching_guides = serializers.SerializerMethodField()

    advance_amount = serializers.ReadOnlyField()

    remaining_amount = serializers.ReadOnlyField()

    available_slots = serializers.SerializerMethodField()

    remaining_slots = serializers.SerializerMethodField()

    adult_total = serializers.SerializerMethodField()

    child_total = serializers.SerializerMethodField()

    infant_total = serializers.SerializerMethodField()

    # =================================
    # META
    # =================================

    class Meta:

        model = Booking

        fields = [

            "id",

            "booking_id",

            "tour",

            "tour_details",

            "guide",

            "selected_guide",

            "guest_name",

            "guest_email",

            "guest_phone",

            "adults",

            "children",

            "infants",

            "tour_date",

            "tour_time",
            "coupon_code",

            "special_requests",

            "payment_method",

            "payment_status",

            "adult_total",

            "child_total",

            "infant_total",

            "sub_total",

            "discount_amount",

            "tax_amount",

            "total_amount",

            "advance_amount",

            "remaining_amount",

            "status",

            "available_slots",

            "remaining_slots",

            "matching_guides",

            "created_at"
        ]

        read_only_fields = [

            "booking_id",

            "payment_status",

            "adult_total",

            "child_total",

            "infant_total",

            "sub_total",

            "discount_amount",

            "tax_amount",

            "total_amount",

            "advance_amount",

            "remaining_amount",

            "status",

            "available_slots",

            "remaining_slots",

            "matching_guides",

            "selected_guide",

            "tour_details",

            "created_at"
        ]

    # =================================
    # VALIDATION
    # =================================

    def validate(self, attrs):

        tour = attrs.get("tour")

        tour_date = attrs.get("tour_date")

        tour_time = attrs.get("tour_time")

        selected_guide = attrs.get("guide")

        adults = attrs.get("adults", 1)

        children = attrs.get("children", 0)

        total_people = adults + children

        # =================================
        # FORMAT TIME
        # =================================

        if isinstance(tour_time, str):

            try:

                tour_time = datetime.strptime(
                    tour_time,
                    "%H:%M"
                ).time()

            except:

                try:

                    tour_time = datetime.strptime(
                        tour_time,
                        "%H:%M:%S"
                    ).time()

                except:

                    raise serializers.ValidationError({

                        "tour_time": (
                            "Invalid time format"
                        )

                    })

        attrs["tour_time"] = tour_time

        # =================================
        # CHECK GUIDE LOCATION
        # =================================

        if selected_guide:

            if not selected_guide.location:

                raise serializers.ValidationError({

                    "guide": (
                        "Guide location missing"
                    )

                })

            # if (

            #     selected_guide.location.strip().lower()

            #     !=

            #     tour.city.strip().lower()

            # ):
            
            if (
                selected_guide.location.strip().lower()
                != tour.city.strip().lower()
                or
                selected_guide.state.strip().lower()
                != tour.state.strip().lower()
            ):

                raise serializers.ValidationError({
                    "guide": (
                        "Selected guide is not available "
                        "for this location"
                    )
                })

                raise serializers.ValidationError({

                    "guide": (

                        "Selected guide is "
                        "not available "
                        "for this city"
                    )

                })

        # =================================
        # CHECK SCHEDULE
        # =================================

        schedule = TourSchedule.objects.filter(

            tour=tour,

            is_active=True,

            start_time__hour=tour_time.hour,

            start_time__minute=tour_time.minute

        ).first()

        if not schedule:

            available_times = TourSchedule.objects.filter(

                tour=tour,

                is_active=True

            ).values_list(

                "start_time",

                flat=True
            )

            raise serializers.ValidationError({

                "tour_time": (

                    f"This tour time is not available. "
                    f"Available times: "
                    f"{list(available_times)}"
                )

            })

        # =================================
        # BOOKED SLOT COUNT
        # =================================

        booked_slots = Booking.objects.filter(

            tour=tour,

            tour_date=tour_date,

            tour_time=tour_time

        ).exclude(

            status="cancelled"

        ).count()

        # =================================
        # SLOT FULL
        # =================================

        if booked_slots >= schedule.available_slots:

            raise serializers.ValidationError({

                "tour_time": (

                    "This slot is fully booked"
                )

            })

        # =================================
        # MAX PEOPLE
        # =================================

        if total_people > tour.max_people:

            raise serializers.ValidationError({

                "adults": (

                    f"Maximum allowed people "
                    f"is {tour.max_people}"
                )

            })

        return attrs
    
    def update(self, instance, validated_data):

        tour = instance.tour

        instance.adults = validated_data.get(
            "adults",
            instance.adults
        )

        instance.children = validated_data.get(
            "children",
            instance.children
        )

        instance.infants = validated_data.get(
            "infants",
            instance.infants
        )

        instance.tour_date = validated_data.get(
            "tour_date",
            instance.tour_date
        )

        instance.tour_time = validated_data.get(
            "tour_time",
            instance.tour_time
        )

        instance.payment_method = validated_data.get(
            "payment_method",
            instance.payment_method
        )

        # =========================
        # PRICING
        # =========================

        adult_price = Decimal("0")
        child_price = Decimal("0")
        infant_price = Decimal("0")

        adult_obj = tour.pricing.filter(
            person_type="adult",
            is_active=True
        ).first()

        child_obj = tour.pricing.filter(
            person_type="child",
            is_active=True
        ).first()

        infant_obj = tour.pricing.filter(
            person_type="infant",
            is_active=True
        ).first()

        if adult_obj:
            adult_price = adult_obj.price

        if child_obj:
            child_price = child_obj.price

        if infant_obj:
            infant_price = infant_obj.price

        adult_total = (
            Decimal(instance.adults)
            * Decimal(adult_price)
        )

        child_total = (
            Decimal(instance.children)
            * Decimal(child_price)
        )

        infant_total = (
            Decimal(instance.infants)
            * Decimal(infant_price)
        )

        sub_total = (
            adult_total +
            child_total +
            infant_total
        )

        # =========================
        # COUPON
        # =========================

        discount_amount = Decimal("0")

        if instance.coupon_applied:

            discount_amount = (
                instance.coupon_applied
                .calculate_discount(
                    sub_total
                )
            )

        total_amount = (
            sub_total -
            discount_amount
        )

        instance.sub_total = sub_total
        instance.discount_amount = discount_amount
        instance.total_amount = total_amount

        instance.save()
        instance.refresh_from_db()
        print("SUBTOTAL =", instance.sub_total)
        print("DISCOUNT =", instance.discount_amount)
        print("TOTAL =", instance.total_amount)
        return instance

    # =================================
    # CREATE BOOKING
    # =================================

    def create(self, validated_data):

        request = self.context.get("request")

        user = None

        if request and request.user.is_authenticated:

            user = request.user

        tour = validated_data.get("tour")

        adults = validated_data.get(
            "adults",
            1
        )

        children = validated_data.get(
            "children",
            0
        )

        infants = validated_data.get(
            "infants",
            0
        )

        # =================================
        # GET PRICES
        # =================================

        adult_pricing = tour.pricing.filter(

            person_type="adult",

            is_active=True

        ).first()

        child_pricing = tour.pricing.filter(

            person_type="child",

            is_active=True

        ).first()

        infant_pricing = tour.pricing.filter(

            person_type="infant",

            is_active=True

        ).first()

        # =================================
        # PRICE VALUES
        # =================================

        adult_price = Decimal(

            adult_pricing.price

        ) if adult_pricing else Decimal("0.00")


        child_price = Decimal(

            child_pricing.price

        ) if child_pricing else Decimal("0.00")


        infant_price = Decimal(

            infant_pricing.price

        ) if infant_pricing else Decimal("0.00")

        # =================================
        # TOTALS
        # =================================

        adult_total = (

            adult_price *

            Decimal(adults)
        )

        child_total = (

            child_price *

            Decimal(children)
        )

        infant_total = (

            infant_price *

            Decimal(infants)
        )

        # =================================
        # SUB TOTAL
        # =================================

        sub_total = (

            adult_total +

            child_total +

            infant_total
        )

        # tax_amount = Decimal("0.00")

        # total_amount = (

        #     sub_total +

        #     tax_amount
        # )
        
        
        tax_amount = Decimal("0.00")

        discount_amount = Decimal("0.00")

        coupon = None

        coupon_code = validated_data.pop(
            "coupon_code",
            None
        )

        if coupon_code:

            try:

                # coupon = Coupon.objects.get(
                #     code=coupon_code.strip().upper()
                # )
                
                coupon = Coupon.objects.filter(
                    code__iexact=coupon_code.strip()
                ).first()
                
                if not coupon:

                    raise serializers.ValidationError({

                        "coupon_code":
                        "Invalid coupon code"

                    })

                if not coupon.is_valid():

                    raise serializers.ValidationError({

                        "coupon_code":
                        "Coupon is expired or inactive"

                    })

                discount_amount = (

                    coupon.calculate_discount(
                        sub_total
                    )

                )

            except Coupon.DoesNotExist:

                raise serializers.ValidationError({

                    "coupon_code":
                    "Invalid coupon code"

                })
                

        total_amount = (

            sub_total

            - discount_amount

            + tax_amount

        )
        
        
        print("SUBTOTAL:", sub_total)

        print("COUPON:", coupon_code)

        print("DISCOUNT:", discount_amount)

        print("TOTAL:", total_amount)

        # =================================
        # CREATE BOOKING
        # =================================
        selected_guide = validated_data.pop(
            "guide",
            None
        )
        booking = Booking.objects.create(
            guide=selected_guide,

            user=user,

            sub_total=sub_total,

            discount_amount=discount_amount,

            tax_amount=tax_amount,

            total_amount=total_amount,

            coupon_applied=coupon,

            payment_status="pending",

            status="pending",

            **validated_data
        )
        
        
        if coupon:

            coupon.used_count += 1

            coupon.save()

            if user:

                CouponUsage.objects.create(

                    coupon=coupon,

                    user=user,

                    booking=booking

                )

        return booking


    # =================================
    # TOUR DETAILS
    # =================================

    def get_tour_details(self, obj):

        return TourSerializer(
            obj.tour
        ).data

    # =================================
    # SELECTED GUIDE
    # =================================

    def get_selected_guide(self, obj):

        if obj.guide:

            return GuideSerializer(
                obj.guide ,
                context=self.context
            ).data

        return None

    # =================================
    # MATCHING GUIDES
    # =================================

    def get_matching_guides(self, obj):

        guides = User.objects.filter(

            role="guide",

            location__iexact=obj.tour.city,
            
            state__iexact=obj.tour.state,

            is_active=True
        )

        return GuideSerializer(

            guides,
            many=True,
            context=self.context

        ).data

    # =================================
    # AVAILABLE SLOTS
    # =================================

    def get_available_slots(self, obj):

        schedule = TourSchedule.objects.filter(

            tour=obj.tour,

            start_time=obj.tour_time,

            is_active=True

        ).first()

        if schedule:

            return schedule.available_slots

        return 0

    # =================================
    # REMAINING SLOTS
    # =================================

    def get_remaining_slots(self, obj):

        schedule = TourSchedule.objects.filter(

            tour=obj.tour,

            start_time=obj.tour_time,

            is_active=True

        ).first()

        if not schedule:

            return 0

        booked_slots = Booking.objects.filter(

            tour=obj.tour,

            tour_date=obj.tour_date,

            tour_time=obj.tour_time

        ).exclude(

            status="cancelled"

        ).count()

        return (

            schedule.available_slots -

            booked_slots
        )

    # =================================
    # ADULT TOTAL
    # =================================

    def get_adult_total(self, obj):

        pricing = obj.tour.pricing.filter(
            person_type="adult"
        ).first()

        if pricing:

            return (
                Decimal(pricing.price) *
                Decimal(obj.adults)
            )

        return Decimal("0.00")

    # =================================
    # CHILD TOTAL
    # =================================

    def get_child_total(self, obj):

        pricing = obj.tour.pricing.filter(
            person_type="child"
        ).first()

        if pricing:

            return (
                Decimal(pricing.price) *
                Decimal(obj.children)
            )

        return Decimal("0.00")

    # =================================
    # INFANT TOTAL
    # =================================

    def get_infant_total(self, obj):

        pricing = obj.tour.pricing.filter(
            person_type="infant"
        ).first()

        if pricing:

            return (
                Decimal(pricing.price) *
                Decimal(obj.infants)
            )

        return Decimal("0.00")




# booking/serializers.py

class BookingUpdateSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Booking

        fields = [

            "adults",

            "children",

            "infants",

            "tour_date",

            "tour_time",

            "guide",

            "payment_method"

        ]
        
        
        
        
        
from rest_framework import serializers
from booking.models import Booking


class BookingListSerializer(
    serializers.ModelSerializer
):

    tour_name = serializers.CharField(
        source="tour.title",
        read_only=True
    )

    guide_name = serializers.SerializerMethodField()
    
    user_role = serializers.CharField(
        source="user.role",
        read_only=True
    )


    class Meta:

        model = Booking

        fields = [

            "id",
            "booking_id",

            "tour_name",

            "guide_name",

            "tour_date",

            "total_amount",

            "status",

            "payment_status",

            "created_at",
            "user_role",

        ]

    def get_guide_name(self, obj):

        if obj.guide:

            return obj.guide.username

        return None
    
from rest_framework.generics import ListAPIView
from .models import *


class CancelReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CancelReason
        fields = ["id", "reason"]

