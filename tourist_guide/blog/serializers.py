# from rest_framework import serializers

# from blog.models import (
#     Blog,
#     BlogCategory
# )


# class BlogCategorySerializer(serializers.ModelSerializer):

#     class Meta:

#         model = BlogCategory

#         fields = [
#             "id",
#             "name",
#             "slug",
#         ]


# class BlogListSerializer(serializers.ModelSerializer):

#     category = BlogCategorySerializer()

#     class Meta:

#         model = Blog

#         fields = [

#             "id",

#             "title",

#             "slug",

#             "short_description",

#             "image",

#             "author",

#             "reading_time",

#             "views",

#             "featured",

#             "created_at",

#             "category",

#         ]


# class BlogDetailSerializer(serializers.ModelSerializer):

#     category = BlogCategorySerializer()

#     class Meta:

#         model = Blog

#         fields = "__all__"



from rest_framework import serializers
from .models import Blog, BlogCategory


class BlogCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogCategory
        fields = [
            "id",
            "name",
            "slug",
        ]


class BlogListSerializer(serializers.ModelSerializer):

    category = BlogCategorySerializer(read_only=True)

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "short_description",
            "image",
            "author",
            "reading_time",
            "views",
            "featured",
            "created_at",
            "category",
        ]


class BlogDetailSerializer(serializers.ModelSerializer):

    category = BlogCategorySerializer(read_only=True)

    related_blogs = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "short_description",
            "description",
            "image",
            "author",
            "reading_time",
            "views",
            "featured",
            "created_at",
            "updated_at",
            "meta_title",
            "meta_description",
            "meta_keywords",
            "category",
            "related_blogs",
        ]

    def get_related_blogs(self, obj):

        blogs = Blog.objects.filter(
            category=obj.category,
            is_active=True
        ).exclude(id=obj.id)[:4]

        return BlogListSerializer(
            blogs,
            many=True,
            context=self.context
        ).data