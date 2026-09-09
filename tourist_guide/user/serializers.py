from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User ,Location,GuideProfile



class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = [
            "id",
            "country",
            "state",
            "district",
            "city",
        ]



# class RegisterSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True)

#     confirm_password = serializers.CharField(write_only=True)

#     locations = serializers.PrimaryKeyRelatedField(
#         queryset=Location.objects.filter(is_active=True),
#         many=True,
#         required=False
#     )

#     class Meta:

#         model = User

#         fields = [
#             "id",
#             "username",
#             "email",
#             "phone_number",
#             "role",
#             "profile_image",
#             "locations",
#             "password",
#             "confirm_password",
#         ]

#     def validate(self, attrs):

#         if attrs["password"] != attrs["confirm_password"]:
#             raise serializers.ValidationError(
#                 {"password": "Passwords do not match"}
#             )

#         if (
#             attrs.get("role") == "guide"
#             and not attrs.get("locations")
#         ):
#             raise serializers.ValidationError(
#                 {
#                     "locations":
#                     "Please select at least one location."
#                 }
#             )

#         return attrs

#     def create(self, validated_data):

#         locations = validated_data.pop(
#             "locations",
#             []
#         )

#         validated_data.pop("confirm_password")

#         password = validated_data.pop("password")

#         user = User(**validated_data)

#         user.set_password(password)
        
#                 # IMPORTANT
#         # User is created only after OTP verification.
#         user.is_verified = True

#         user.save()

#         user.locations.set(locations)

#         return user


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True
    )

    confirm_password = serializers.CharField(
        write_only=True,
        required=True
    )

    locations = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.filter(is_active=True),
        many=True,
        required=False
    )

    bio = serializers.CharField(
        required=False,
        allow_blank=True
    )

    experience_years = serializers.IntegerField(
        required=False,
        min_value=0
    )

    languages = serializers.CharField(
        required=False,
        allow_blank=True
    )

    # Aadhaar files
    aadhaar_front = serializers.ImageField(
        required=False,
        allow_null=False
    )

    aadhaar_back = serializers.ImageField(
        required=False,
        allow_null=False
    )

    # Certificate optional
    certificates = serializers.FileField(
        required=False,
        allow_null=True
    )

    class Meta:

        model = User

        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "role",
            "profile_image",

            "locations",

            "password",
            "confirm_password",

            "bio",
            "experience_years",
            "languages",

            "aadhaar_front",
            "aadhaar_back",
            "certificates",
        ]

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(self, attrs):

        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:

            raise serializers.ValidationError({
                "password": "Passwords do not match."
            })

        role = attrs.get("role")

        locations = attrs.get(
            "locations",
            []
        )

        # =================================================
        # GUIDE VALIDATION
        # =================================================

        if role == "guide":

            if not locations:

                raise serializers.ValidationError({
                    "locations":
                        "Please select at least one location."
                })

            # Aadhaar FRONT mandatory
            if not attrs.get("aadhaar_front"):

                raise serializers.ValidationError({
                    "aadhaar_front":
                        "Aadhaar front document is required."
                })

            # Aadhaar BACK mandatory
            if not attrs.get("aadhaar_back"):

                raise serializers.ValidationError({
                    "aadhaar_back":
                        "Aadhaar back document is required."
                })

            languages = attrs.get(
                "languages",
                ""
            ).strip()

            if not languages:

                raise serializers.ValidationError({
                    "languages":
                        "Please enter your languages."
                })

        return attrs

    # =====================================================
    # CREATE USER + GUIDE PROFILE
    # =====================================================

    def create(self, validated_data):

        # Remove guide-specific fields
        bio = validated_data.pop(
            "bio",
            ""
        )

        experience_years = validated_data.pop(
            "experience_years",
            0
        )

        languages = validated_data.pop(
            "languages",
            ""
        )

        aadhaar_front = validated_data.pop(
            "aadhaar_front",
            None
        )

        aadhaar_back = validated_data.pop(
            "aadhaar_back",
            None
        )

        certificates = validated_data.pop(
            "certificates",
            None
        )

        locations = validated_data.pop(
            "locations",
            []
        )

        # Remove confirm password
        validated_data.pop(
            "confirm_password",
            None
        )

        # Password
        password = validated_data.pop(
            "password"
        )

        # =================================================
        # CREATE USER
        # =================================================

        user = User(
            **validated_data
        )

        user.set_password(password)

        user.is_verified = True

        user.save()

        # =================================================
        # LOCATIONS
        # =================================================

        if locations:

            user.locations.set(
                locations
            )

        # =================================================
        # GUIDE PROFILE
        # =================================================

        if user.role == "guide":

            GuideProfile.objects.create(

                user=user,

                bio=bio,

                experience_years=experience_years,

                languages=languages,

                aadhaar_front=aadhaar_front,

                aadhaar_back=aadhaar_back,

                certificates=certificates,

                verification_status="pending"
            )

        return user


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            email=email,
            password=password
        )

        if not user:

            raise serializers.ValidationError(
                'Invalid email or password'
            )

        attrs['user'] = user

        return attrs
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
from rest_framework import serializers
from .models import User



from rest_framework import serializers

from .models import User, Location

from rest_framework import serializers

from .models import User, Location

from rest_framework import serializers

from .models import User, Location


# ============================================================
# LOCATION SERIALIZER
# ============================================================

class LocationSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Location

        fields = [
            "id",
            "country",
            "state",
            "district",
            "city",
        ]


# ============================================================
# PROFILE SERIALIZER
# ============================================================

class ProfileSerializer(
    serializers.ModelSerializer
):

    profile_image = serializers.SerializerMethodField()

    locations = serializers.SerializerMethodField()

    country = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()



        # ========================================================
    # GUIDE FIELDS
    # ========================================================

    bio = serializers.SerializerMethodField()

    experience_years = serializers.SerializerMethodField()

    languages = serializers.SerializerMethodField()

    aadhaar_front = serializers.SerializerMethodField()

    aadhaar_back = serializers.SerializerMethodField()

    certificates = serializers.SerializerMethodField()
    class Meta:

        model = User

        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "role",

            "locations",

            "country",
            "state",
            "district",
            "city",
            
            
            # Guide details
            "bio",
            "experience_years",
            "languages",

            # Guide documents
            "aadhaar_front",
            "aadhaar_back",
            "certificates",

            "profile_image",

            "is_verified",
            "created_at",
        ]


    # ========================================================
    # PROFILE IMAGE
    # ========================================================

    def get_profile_image(
        self,
        obj
    ):

        request = self.context.get(
            "request"
        )


        if (
            obj.profile_image
            and hasattr(
                obj.profile_image,
                "url"
            )
        ):

            image_url = (
                obj.profile_image.url
            )


            if request:

                return request.build_absolute_uri(
                    image_url
                )


            return image_url


        return None


    # ========================================================
    # LOCATIONS
    #
    # ONLY GUIDE
    # ========================================================

    def get_locations(
        self,
        obj
    ):

        if obj.role != "guide":

            return []


        return LocationSerializer(
            obj.locations.all(),
            many=True
        ).data


    # ========================================================
    # COUNTRY
    #
    # ONLY GUIDE
    # ========================================================

    def get_country(
        self,
        obj
    ):

        if obj.role != "guide":

            return None


        location = (
            obj.locations.first()
        )


        if location:

            return location.country


        return None


    # ========================================================
    # STATE
    #
    # ONLY GUIDE
    # ========================================================

    def get_state(
        self,
        obj
    ):

        if obj.role != "guide":

            return None


        location = (
            obj.locations.first()
        )


        if location:

            return location.state


        return None


    # ========================================================
    # DISTRICT
    #
    # ONLY GUIDE
    # ========================================================

    def get_district(
        self,
        obj
    ):

        if obj.role != "guide":

            return None


        location = (
            obj.locations.first()
        )


        if location:

            return location.district


        return None


    # ========================================================
    # CITY
    #
    # ONLY GUIDE
    # ========================================================

    def get_city(
        self,
        obj
    ):

        if obj.role != "guide":

            return None


        location = (
            obj.locations.first()
        )


        if location:

            return location.city


        return None
    
    
       # ========================================================
    # GUIDE BIO
    # ========================================================

    def get_bio(
        self,
        obj
    ):

        if (
            obj.role == "guide"
            and hasattr(
                obj,
                "guide_profile"
            )
        ):

            return (
                obj.guide_profile.bio
                or ""
            )

        return ""


    # ========================================================
    # EXPERIENCE
    # ========================================================

    def get_experience_years(
        self,
        obj
    ):

        if (
            obj.role == "guide"
            and hasattr(
                obj,
                "guide_profile"
            )
        ):

            return (
                obj.guide_profile.experience_years
                or 0
            )

        return 0


    # ========================================================
    # LANGUAGES
    # ========================================================

    def get_languages(
        self,
        obj
    ):

        if (
            obj.role == "guide"
            and hasattr(
                obj,
                "guide_profile"
            )
        ):

            return (
                obj.guide_profile.languages
                or ""
            )

        return ""


    # ========================================================
    # AADHAAR FRONT
    # ========================================================

    def get_aadhaar_front(
        self,
        obj
    ):

        if (
            obj.role == "guide"
            and hasattr(
                obj,
                "guide_profile"
            )
        ):

            document = (
                obj.guide_profile.aadhaar_front
            )

            if document:

                request = self.context.get(
                    "request"
                )

                if request:

                    return request.build_absolute_uri(
                        document.url
                    )

                return document.url

        return None


    # ========================================================
    # AADHAAR BACK
    # ========================================================

    def get_aadhaar_back(
        self,
        obj
    ):

        if (
            obj.role == "guide"
            and hasattr(
                obj,
                "guide_profile"
            )
        ):

            document = (
                obj.guide_profile.aadhaar_back
            )

            if document:

                request = self.context.get(
                    "request"
                )

                if request:

                    return request.build_absolute_uri(
                        document.url
                    )

                return document.url

        return None


    # ========================================================
    # CERTIFICATES
    # ========================================================

    def get_certificates(
        self,
        obj
    ):

        if (
            obj.role == "guide"
            and hasattr(
                obj,
                "guide_profile"
            )
        ):

            document = (
                obj.guide_profile.certificates
            )

            if document:

                request = self.context.get(
                    "request"
                )

                if request:

                    return request.build_absolute_uri(
                        document.url
                    )

                return document.url

        return None



# ============================================================
# PROFILE UPDATE SERIALIZER
# ============================================================

class ProfileUpdateSerializer(
    serializers.ModelSerializer
):

    locations = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.filter(
            is_active=True
        ),
        many=True,
        required=False
    )

    # ========================================================
    # GUIDE FIELDS
    # ========================================================

    bio = serializers.CharField(
        required=False,
        allow_blank=True
    )

    experience_years = serializers.IntegerField(
        required=False,
        min_value=0
    )

    languages = serializers.CharField(
        required=False,
        allow_blank=True
    )

    aadhaar_front = serializers.ImageField(
        required=False,
        allow_null=True
    )

    aadhaar_back = serializers.ImageField(
        required=False,
        allow_null=True
    )

    certificates = serializers.FileField(
        required=False,
        allow_null=True
    )


    class Meta:

        model = User

        fields = [

            # Normal User fields
            "username",
            "phone_number",
            "profile_image",

            # Location
            "locations",

            # Guide fields
            "bio",
            "experience_years",
            "languages",

            # Documents
            "aadhaar_front",
            "aadhaar_back",
            "certificates",
        ]


    # ========================================================
    # UPDATE
    # ========================================================

    def update(
        self,
        instance,
        validated_data
    ):

        # ====================================================
        # GET LOCATIONS
        # ====================================================

        locations = validated_data.pop(
            "locations",
            None
        )


        # ====================================================
        # GET GUIDE FIELDS
        # ====================================================

        bio = validated_data.pop(
            "bio",
            None
        )

        experience_years = validated_data.pop(
            "experience_years",
            None
        )

        languages = validated_data.pop(
            "languages",
            None
        )

        aadhaar_front = validated_data.pop(
            "aadhaar_front",
            None
        )

        aadhaar_back = validated_data.pop(
            "aadhaar_back",
            None
        )

        certificates = validated_data.pop(
            "certificates",
            None
        )


        # ====================================================
        # UPDATE NORMAL USER FIELDS
        # ====================================================

        for field, value in validated_data.items():

            setattr(
                instance,
                field,
                value
            )


        instance.save()


        # ====================================================
        # GUIDE
        # ====================================================

        if instance.role == "guide":

            guide_profile, created = (
                GuideProfile.objects.get_or_create(
                    user=instance
                )
            )


            # ------------------------------------------------
            # BIO
            # ------------------------------------------------

            if bio is not None:

                guide_profile.bio = bio


            # ------------------------------------------------
            # EXPERIENCE
            # ------------------------------------------------

            if experience_years is not None:

                guide_profile.experience_years = (
                    experience_years
                )


            # ------------------------------------------------
            # LANGUAGES
            # ------------------------------------------------

            if languages is not None:

                guide_profile.languages = (
                    languages
                )


            # ------------------------------------------------
            # AADHAAR FRONT
            # Only replace when new file uploaded
            # ------------------------------------------------

            if aadhaar_front is not None:

                guide_profile.aadhaar_front = (
                    aadhaar_front
                )


            # ------------------------------------------------
            # AADHAAR BACK
            # Only replace when new file uploaded
            # ------------------------------------------------

            if aadhaar_back is not None:

                guide_profile.aadhaar_back = (
                    aadhaar_back
                )


            # ------------------------------------------------
            # CERTIFICATES
            # Only replace when new file uploaded
            # ------------------------------------------------

            if certificates is not None:

                guide_profile.certificates = (
                    certificates
                )


            guide_profile.save()


            # ------------------------------------------------
            # LOCATIONS
            # ------------------------------------------------

            if locations is not None:

                instance.locations.set(
                    locations
                )


        # ====================================================
        # TOURIST / ADMIN
        # ====================================================

        else:

            instance.locations.clear()


        return instance
# class ProfileUpdateSerializer(
#     serializers.ModelSerializer
# ):

#     locations = serializers.PrimaryKeyRelatedField(
#         queryset=Location.objects.filter(
#             is_active=True
#         ),
#         many=True,
#         required=False
#     )


#     # ========================================================
#     # GUIDE FIELDS
#     # ========================================================

#     bio = serializers.CharField(
#         required=False,
#         allow_blank=True
#     )

#     experience_years = serializers.IntegerField(
#         required=False,
#         min_value=0
#     )

#     languages = serializers.CharField(
#         required=False,
#         allow_blank=True
#     )

#     aadhaar_front = serializers.ImageField(
#         required=False,
#         allow_null=True
#     )

#     aadhaar_back = serializers.ImageField(
#         required=False,
#         allow_null=True
#     )

#     certificates = serializers.FileField(
#         required=False,
#         allow_null=True
#     )


#     class Meta:

#         model = User

#         fields = [
#             "username",
#             "phone_number",
#             "profile_image",
#             "locations",
            
            
#                         # Guide fields
#             "bio",
#             "experience_years",
#             "languages",

#             # Documents
#             "aadhaar_front",
#             "aadhaar_back",
#             "certificates",
#         ]


#     # ========================================================
#     # UPDATE
#     # ========================================================

#     def update(
#         self,
#         instance,
#         validated_data
#     ):

#         locations = validated_data.pop(
#             "locations",
#             None
#         )


#         # ====================================================
#         # UPDATE NORMAL USER FIELDS
#         # ====================================================

#         for field, value in validated_data.items():

#             setattr(
#                 instance,
#                 field,
#                 value
#             )


#         instance.save()


#         # ====================================================
#         # GUIDE
#         # ====================================================

#         if instance.role == "guide":

#             if locations is not None:

#                 instance.locations.set(
#                     locations
#                 )


#         # ====================================================
#         # TOURIST / ADMIN
#         # ====================================================

#         else:

#             instance.locations.clear()


#         return instance