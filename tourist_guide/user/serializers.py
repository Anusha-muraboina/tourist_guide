from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User ,Location



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



class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    confirm_password = serializers.CharField(write_only=True)

    locations = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.filter(is_active=True),
        many=True,
        required=False
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
        ]

    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Passwords do not match"}
            )

        if (
            attrs.get("role") == "guide"
            and not attrs.get("locations")
        ):
            raise serializers.ValidationError(
                {
                    "locations":
                    "Please select at least one location."
                }
            )

        return attrs

    def create(self, validated_data):

        locations = validated_data.pop(
            "locations",
            []
        )

        validated_data.pop("confirm_password")

        password = validated_data.pop("password")

        user = User(**validated_data)

        user.set_password(password)

        user.save()

        user.locations.set(locations)

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


    class Meta:

        model = User

        fields = [
            "username",
            "phone_number",
            "profile_image",
            "locations",
        ]


    # ========================================================
    # UPDATE
    # ========================================================

    def update(
        self,
        instance,
        validated_data
    ):

        locations = validated_data.pop(
            "locations",
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