from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from home.views import CustomSignupView, custom_404_view
from home.sitemaps import StaticViewSitemap, ProductSitemap

# ─── SITEMAP DICTIONARY ────
sitemaps = {
    "static": StaticViewSitemap(),
    "products": ProductSitemap(),
}
# ───────────────────────────────────────────

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/signup/", CustomSignupView.as_view(), name="account_signup"
    ),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("home.urls")),
    path("", include("newsletter.urls")),
    path("products/", include("products.urls")),
    path("orders/", include("orders.urls")),
    path("users/", include("users.urls")),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt", content_type="text/plain"
        ),
    ),
    # only one sitemap.xml entry, passing just the `sitemaps` dict:
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="sitemap",
    ),
]

handler404 = custom_404_view

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
