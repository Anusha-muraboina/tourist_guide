from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from tourist.models import Tour
from blog.models import Blog


# =====================================================
# STATIC PAGES
# =====================================================

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "tourlist",
            "about_us",
            "terms",
            "policy",
            "contact",
        ]

    def location(self, item):
        return reverse(item)


# =====================================================
# TOUR SITEMAP
# =====================================================

class TourSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return Tour.objects.filter(
            is_active=True
        )

    def location(self, obj):
        return reverse(
            "tour_details",
            kwargs={
                "slug": obj.slug,
            },
        )


# =====================================================
# BLOG SITEMAP
# =====================================================

class BlogSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Blog.objects.filter(
            is_active=True
        ).order_by("-updated_at")

    def location(self, obj):
        return reverse(
            "blog_detail",
            kwargs={
                "slug": obj.slug,
            },
        )

    def lastmod(self, obj):
        return obj.updated_at