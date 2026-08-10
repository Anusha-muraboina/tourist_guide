# tours/api/serializers.py

from rest_framework import serializers
from django.db.models import Avg
from tourist.models import (
    Tour,
    TourImage,
    TourHighlight,
    TourInclude,
    TourExclude,
    ImportantInformation,
    TourSchedule,
    Amenity,
)

from user.serializers import LocationSerializer
from rating.serializers import RatingSerializer

from user.models import User

# =========================================
# TOUR IMAGE
# =========================================
from rest_framework import serializers
from tourist.models import TourCategory


class TourCategorySerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = TourCategory
        fields = [
            "id",
            "name"
        ]
class TourImageSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:

        model = TourImage

        fields = [
            "id",
            "image",
            "is_primary",
        ]

    def get_image(self, obj):

        request = self.context.get("request")

        if obj.image and request:

            return request.build_absolute_uri(
                obj.image.url
            )

        return None


# =========================================
# TOUR HIGHLIGHT
# =========================================

class TourHighlightSerializer(serializers.ModelSerializer):

    class Meta:

        model = TourHighlight

        fields = [
            "id",
            "title",
            "slot_position",
        ]


# =========================================
# TOUR INCLUDE
# =========================================

class TourIncludeSerializer(serializers.ModelSerializer):

    class Meta:

        model = TourInclude

        fields = [
            "id",
            "title",
            "slot_position",
        ]


# =========================================
# TOUR EXCLUDE
# =========================================

class TourExcludeSerializer(serializers.ModelSerializer):

    class Meta:

        model = TourExclude

        fields = [
            "id",
            "title",
            "slot_position",
        ]


# =========================================
# IMPORTANT INFORMATION
# =========================================

class ImportantInformationSerializer(serializers.ModelSerializer):

    class Meta:

        model = ImportantInformation

        fields = [
            "id",
            "title",
            "slot_position",
        ]


# =========================================
# TOUR SCHEDULE
# =========================================

class TourScheduleSerializer(serializers.ModelSerializer):

    class Meta:

        model = TourSchedule

        fields = [
            "id",
            "start_time",
            # "end_time",
            "available_slots",
            "is_active",
        ]


# =========================================
# AMENITY
# =========================================

class AmenitySerializer(serializers.ModelSerializer):

    class Meta:

        model = Amenity

        fields = [
            "id",
            "name",
            "icon_class",
            "slot_position",
        ]


# =========================================
# TOUR LIST SERIALIZER
# =========================================

# class TourListSerializer(serializers.ModelSerializer):

#     thumbnail = serializers.SerializerMethodField()

#     final_price = serializers.ReadOnlyField()

#     class Meta:

#         model = Tour

#         fields = [

#             "id",
#             "title",
#             "slug",
#             "tour_type",
#             "duration",
#             # "price",
#             # "offer_price",
#             "final_price",
#             "featured",
#             "thumbnail",

#         ]

#     def get_thumbnail(self, obj):

#         image = obj.images.first()

#         if image:

#             request = self.context.get("request")

#             return request.build_absolute_uri(
#                 image.image.url
#             )

#         return None


from rest_framework import serializers

from tourist.models import (
    Tour,
    TourImage,
    TourPricing
)
class TourPricingSerializer(serializers.ModelSerializer):

    class Meta:

        model = TourPricing

        fields = [
            "id",
            "person_type",
            "price",
        ]

class TourListSerializer(
    serializers.ModelSerializer
):

    thumbnail = serializers.SerializerMethodField()

    adult_price = serializers.SerializerMethodField()
    
    location = LocationSerializer(read_only=True)

    class Meta:

        model = Tour

        fields = [

            "id",

            "title",

            "slug",
            # "state",
            "location",
            "tour_type",
            "short_description",

            "duration",

            "adult_price",

            "featured",

            "thumbnail",
        ]

    # ==========================
    # THUMBNAIL
    # ==========================

    def get_thumbnail(self, obj):

        image = obj.images.first()

        if image:

            request = self.context.get(
                "request"
            )

            if request:

                return request.build_absolute_uri(
                    image.image.url
                )

        return None

    # ==========================
    # ADULT PRICE
    # ==========================

    def get_adult_price(self, obj):

        pricing = obj.pricing.filter(

            person_type="adult",

            is_active=True

        ).first()

        if pricing:

            return pricing.price

        return 0


# =========================================
# TOUR DETAIL SERIALIZER
# =========================================

class TourDetailSerializer(serializers.ModelSerializer):

    images = TourImageSerializer(
        many=True,
        read_only=True
    )
    pricing = TourPricingSerializer(
        many=True,
        read_only=True
    )
    highlights = TourHighlightSerializer(
        many=True,
        read_only=True
    )

    includes = TourIncludeSerializer(
        many=True,
        read_only=True
    )

    excludes = TourExcludeSerializer(
        many=True,
        read_only=True
    )

    important_information = ImportantInformationSerializer(
        many=True,
        read_only=True
    )

    schedules = TourScheduleSerializer(
        many=True,
        read_only=True
    )

    amenities = AmenitySerializer(
        many=True,
        read_only=True
    )

    final_price = serializers.ReadOnlyField()
    
    guides = serializers.SerializerMethodField()
    
    
    
    average_rating = serializers.SerializerMethodField()

    total_ratings = serializers.SerializerMethodField()

    reviews = serializers.SerializerMethodField()
    
    location = LocationSerializer(read_only=True)

    class Meta:

        model = Tour

        fields = [

            "id",
            "title",
            "slug",
            "short_description",
            "full_description",
            "pricing",
             "guides",
            # "city",
            # "state",
            # "country",
            # "address",
            
            "location",
            "meeting_point",
            "duration",
            "language",
            "tour_type",

            "max_people",
            "min_age",
            # "price",
            # "offer_price",
            "final_price",
            "free_cancellation",
            "instant_confirmation",
            "pickup_available",
            "wheelchair_accessible",
            "featured",
            "is_active",
            "images",
            "highlights",
            "includes",
            "excludes",
            "important_information",
            "schedules",
            "amenities",
            
            "average_rating",
            "total_ratings",
            "reviews",

            "created_at",
            "updated_at",
        ]
        
    def get_guides(self, obj):

        request = self.context.get("request")

        if not obj.location:
            return []

        guides = User.objects.filter(
            role="guide",
            is_active=True,
            locations=obj.location
        ).distinct()

        return [
            {
                "id": guide.id,
                "name": guide.username,
                "email": guide.email,
                "phone": guide.phone_number,
                "locations": [
                    {
                        "id": loc.id,
                        "city": loc.city,
                        "district": loc.district,
                        "state": loc.state,
                        "country": loc.country,
                    }
                    for loc in guide.locations.all()
                ],
                "profile_image": (
                    request.build_absolute_uri(guide.profile_image.url)
                    if guide.profile_image and request
                    else None
                ),
            }
            for guide in guides
        ]
        
        
    # def get_guides(self, obj):
    #     request = self.context.get("request")

    #     # Correct filter using ManyToMany locations
    #     guides = User.objects.filter(
    #         role="guide",
    #         is_active=True,
    #         locations__city__iexact=obj.city,
    #         locations__state__iexact=obj.state,
    #     ).distinct()

    #     return [
    #         {
    #             "id": guide.id,
    #             "name": guide.username,
    #             "email": guide.email,
    #             "phone": guide.phone_number,
    #             "locations": [
    #                 {
    #                     "id": loc.id,
    #                     "city": loc.city,
    #                     "district": loc.district,
    #                     "state": loc.state,
    #                     "country": loc.country,
    #                 }
    #                 for loc in guide.locations.all()
    #             ],
    #             "profile_image": (
    #                 request.build_absolute_uri(guide.profile_image.url)
    #                 if guide.profile_image and request
    #                 else None
    #             ),
    #         }
    #         for guide in guides
    #     ]
        
    # def get_guides(self, obj):

    #     request = self.context.get("request")

    #     guides = User.objects.filter(
    #         role="guide",
    #         location__iexact=obj.city,
    #         state__iexact=obj.state,
    #         is_active=True
    #     )

    #     return [
    #         {
    #             "id": guide.id,
    #             "name": guide.username,
    #             "email": guide.email,
    #             "phone": guide.phone_number,
    #             "location": guide.location,
    #             "state": guide.state,
    #             "profile_image":
    #                 request.build_absolute_uri(
    #                     guide.profile_image.url
    #                 )
    #                 if guide.profile_image and request
    #                 else None
    #         }
    #         for guide in guides
    #     ]
        
    def get_average_rating(self, obj):

            avg = obj.ratings.filter(
                active=True
            ).aggregate(
                Avg("rating")
            )["rating__avg"]

            return round(avg, 1) if avg else 0


    def get_total_ratings(self, obj):

            return obj.ratings.filter(
                active=True
            ).count()


    def get_reviews(self, obj):

            ratings = obj.ratings.filter(
                active=True
            ).order_by(
                "-created_at"
            )[:10]

            return RatingSerializer(
                ratings,
                many=True
            ).data
        
    # def get_guides(self, obj):

    #     guides = User.objects.filter(

    #         role="guide",

    #         location__iexact=obj.city,

    #         is_active=True

    #     )

    #     return [

    #         {
    #             "id": guide.id,
    #             "name": guide.username,
    #             "email": guide.email,
    #             "phone": guide.phone_number,
    #             "location": guide.location,
    #         }

    #         for guide in guides
    #     ]
        
        
        
from rest_framework import serializers
from tourist.models import Tour, TourCategory


class TourCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = [
            "id",
            "title",
            "slug",
            "adult_price",
            "image"
        ]

    def get_image(self, obj):

        image = obj.images.filter(
            is_primary=True
        ).first()

        if not image:
            image = obj.images.first()

        return image.image.url if image else None


class CategorySerializer(serializers.ModelSerializer):

    tours = TourCardSerializer(
        many=True,
        read_only=True,
        source="tours"
    )

    class Meta:
        model = TourCategory
        fields = [
            "id",
            "name",
            "tours"
        ]
        
        
        
        
        
        
        
