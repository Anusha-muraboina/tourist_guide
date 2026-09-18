

from rest_framework import serializers
from .models import ContactUs


# class ContactUsSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = ContactUs
#         fields = "__all__"
#         read_only_fields = (
#             "id",
#             "is_read",
#             "created_at",
#         )



from rest_framework import serializers
from .models import ContactUs


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ["name", "email", "phone_number", "message"]