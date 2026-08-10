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





# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(
#         write_only=True
#     )
#     confirm_password = serializers.CharField(
#         write_only=True
#     )
#     class Meta:

#         model = User

#         fields = [
#             'id',
#             'username',
#             'email',
#             'phone_number',
#             'location',
#              "state",

#             "country",
#             'profile_image',
#             'role',
#             'password',
#             'confirm_password',
#         ]

#     def validate(self, attrs):

#         if attrs['password'] != attrs['confirm_password']:

#             raise serializers.ValidationError(
#                 {
#                     'password': 'Passwords do not match'
#                 }
#             )

#         return attrs

#     def create(self, validated_data):

#         validated_data.pop('confirm_password')

#         password = validated_data.pop('password')

#         user = User(**validated_data)

#         user.set_password(password)

#         user.save()

#         return user




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

# class ProfileSerializer(serializers.ModelSerializer):

#     profile_image = serializers.SerializerMethodField()
    
#     locations = LocationSerializer(
#         many=True,
#         read_only=True
#     )

#     class Meta:

#         model = User

#         fields = [
#             "id",
#             "username",
#             "email",
#             "phone_number",
#             # "location",
#             # "state",
#             # "country",
#             "role",
#             "locations",
#             "profile_image",
#             "is_verified",
#             "created_at"
#         ]

#     def get_profile_image(self, obj):

#         request = self.context.get("request")

#         if obj.profile_image:

#             return request.build_absolute_uri(
#                 obj.profile_image.url
#             )

#         return None



class ProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    locations = LocationSerializer(many=True, read_only=True)

    # Convenience fields (optional but useful for frontend)
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
            "role",                     # ← role
            "locations",                # ← full list of locations
            "country",                  # ← from first location
            "state",                    # ← from first location
            "district",                 # ← from first location
            "city",                     # ← from first location
            "profile_image",
            "is_verified",
            "created_at",
        ]

    def get_profile_image(self, obj):
        request = self.context.get("request")
        if obj.profile_image and hasattr(obj.profile_image, "url"):
            return request.build_absolute_uri(obj.profile_image.url)
        return None

    def get_country(self, obj):
        loc = obj.locations.first()
        return loc.country if loc else None

    def get_state(self, obj):
        loc = obj.locations.first()
        return loc.state if loc else None

    def get_district(self, obj):
        loc = obj.locations.first()
        return loc.district if loc else None

    def get_city(self, obj):
        loc = obj.locations.first()
        return loc.city if loc else None

# class ProfileUpdateSerializer(
# serializers.ModelSerializer
# ):

#     locations = serializers.PrimaryKeyRelatedField(
#         queryset=Location.objects.filter(is_active=True),
#         many=True,
#         required=False
#     )

#     class Meta:

#         model = User

#         fields = [
#             "username",
#             "phone_number",
#             "location",
#             "state",
#             "country",
#             "profile_image",
#             "locations",
#         ]
    
#     def update(self, instance, validated_data):

#         locations = validated_data.pop(
#             "locations",
#             None
#         )

#         instance = super().update(
#             instance,
#             validated_data
#         )

#         if locations is not None:
#             instance.locations.set(locations)

#         return instance


class ProfileUpdateSerializer(
    serializers.ModelSerializer
):

    locations = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.filter(is_active=True),
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

    def update(
        self,
        instance,
        validated_data
    ):

        locations = validated_data.pop(
            "locations",
            None
        )

        instance = super().update(
            instance,
            validated_data
        )

        if locations is not None:
            instance.locations.set(locations)

        return instance