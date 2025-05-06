from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from home.views import CustomSignupView, custom_404_view
from home.sitemaps import StaticViewSitemap, ProductSitemap

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/signup/", CustomSignupView.as_view(), name="account_signup"),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("home.urls")),         # Homepage URL
    path("", include("newsletter.urls")),   # Newsletter app
    path("products/", include("products.urls")),  # Products app
    path("orders/", include("orders.urls")),      # Orders app
    path("users/", include("users.urls")),        # Users app
]

# Serve robots.txt
urlpatterns += [
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain"
        ),
    ),
]

# Sitemap configuration
sitemaps = {
    "static": StaticViewSitemap(),
    "products": ProductSitemap(),
}

# Override domain & protocol for sitemap URLs
urlpatterns += [
    path(
        "sitemap.xml",
        sitemap,
        {
            "sitemaps": sitemaps,
            "protocol": "https",
            "domain": "cake-factory-65cd55cbb35d.herokuapp.com",
        },
        name="sitemap",
    ),
]

# Custom 404 handler
handler404 = custom_404_view

# Serve media files in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )