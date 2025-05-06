from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from products.models import Product

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
            "edit_profile",
        ]

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return Product.objects.filter(available=True)

    def location(self, item):
        # Use the named URL so slugs appear instead of IDs
        return reverse("product_detail", args=[item.slug])