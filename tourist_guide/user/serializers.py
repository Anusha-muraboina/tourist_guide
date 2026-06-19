from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    class Meta:

        model = User

        fields = [
            'id',
            'username',
            'email',
            'phone_number',
            'location',
             "state",

            "country",
            'profile_image',
            'role',
            'password',
            'confirm_password',
        ]

    def validate(self, attrs):

        if attrs['password'] != attrs['confirm_password']:

            raise serializers.ValidationError(
                {
                    'password': 'Passwords do not match'
                }
            )

        return attrs

    def create(self, validated_data):

        validated_data.pop('confirm_password')

        password = validated_data.pop('password')

        user = User(**validated_data)

        user.set_password(password)

        user.save()

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