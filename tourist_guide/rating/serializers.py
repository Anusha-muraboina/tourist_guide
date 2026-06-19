

from rest_framework import serializers
from rating.models import Rating

from rating.serializers import RatingSerializer
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