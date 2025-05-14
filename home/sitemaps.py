from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from django.conf import settings
from products.models import Product
from types import SimpleNamespace


def get_site_namespace():
    """Ensure valid domain and protocol for sitemap entries."""
    domain = getattr(settings, "SITEMAP_DOMAIN", None)
    protocol = getattr(settings, "SITEMAP_PROTOCOL", "https")

    # Fallback to SITE_URL if domain is missing
    if not domain:
        domain = getattr(settings, "SITE_URL", "example.com").replace("https://", "").replace("http://", "").rstrip("/")

    return SimpleNamespace(domain=domain, name="Cake Factory"), protocol


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
        site, protocol = get_site_namespace()
        return super().get_urls(site=site, protocol=protocol)


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Product.objects.filter(available=True).order_by("id")

    def location(self, item):
        return f"/products/{item.slug}/"

    def get_urls(self, site=None, **kwargs):
        site, protocol = get_site_namespace()
        return super().get_urls(site=site, protocol=protocol)
