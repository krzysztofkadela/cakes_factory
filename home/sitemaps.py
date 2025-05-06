from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from django.conf import settings
from products.models import Product
from types import SimpleNamespace

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

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
        return reverse(item)

    def get_urls(self, site=None, **kwargs):
        if site is None:
            site = SimpleNamespace(
                domain=settings.SITEMAP_DOMAIN,
                name="Cake Factory"
            )
        return super().get_urls(site=site, protocol=settings.SITEMAP_PROTOCOL)


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Product.objects.filter(available=True)

    def location(self, item):
        return f"/products/{item.slug}/"

    def get_urls(self, site=None, **kwargs):
        if site is None:
            site = SimpleNamespace(
                domain=settings.SITEMAP_DOMAIN,
                name="Cake Factory"
            )
        return super().get_urls(site=site, protocol=settings.SITEMAP_PROTOCOL)