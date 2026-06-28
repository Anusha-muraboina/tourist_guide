

from rest_framework import serializers
from rating.models import Rating


class RatingSerializer(serializers.ModelSerializer):

    user_name = serializers.SerializerMethodField()

    class Meta:

        model = Rating

        fields = [
            "id",
            "rating",
            "review",
            "created_at",
            "user_name"
        ]

    def get_user_name(self, obj):

        if obj.anonymous:
            return "Anonymous"

        return obj.user.username
    
    
from rest_framework import serializers
from rating.models import Rating

class RatingCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = [
            "tour",
            "rating",
            "review",
            "anonymous",
        ]