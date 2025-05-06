from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from django.conf import settings
from products.models import Product
from types import SimpleNamespace

class StaticViewSitemap(Sitemap):
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
            "edit_profile"
        ]

    def location(self, item):
        return reverse(item)

    def get_urls(self, site=None, **kwargs):
        if not site:
            domain = settings.SITE_URL.replace("https://", "").replace("http://", "").rstrip("/")
            site = SimpleNamespace(domain=domain, name="Cake Factory")
        return super().get_urls(site=site, **kwargs)


class ProductSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return Product.objects.filter(available=True)

    def location(self, item):
        return f"/products/{item.slug}/"

    def get_urls(self, site=None, **kwargs):
        if not site:
            domain = settings.SITE_URL.replace("https://", "").replace("http://", "").rstrip("/")
            site = SimpleNamespace(domain=domain, name="Cake Factory")
        return super().get_urls(site=site, **kwargs)