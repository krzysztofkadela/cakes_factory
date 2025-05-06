from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.conf import settings
from products.models import Product


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return [
            "home",
            "cart_view",
            "checkout",
            "order_history",
            "payment_success",
            "payment_cancel",
            "user_profile",
            "edit_profile",
        ]

    def location(self, item):
        # Prefix with the site URL to ensure correct domain in production
        return f"{settings.SITE_URL}{reverse(item)}"


class ProductSitemap(Sitemap):
    """Sitemap for product pages"""
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return Product.objects.filter(available=True)

    def location(self, item):
        # Use named URL for product detail and prefix with site URL
        return f"{settings.SITE_URL}{reverse('product_detail', args=[item.pk])}"