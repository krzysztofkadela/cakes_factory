from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (
            "Shipping Information",
            {
                "fields": (
                    "shipping_full_name",
                    "shipping_phone",
                    "shipping_street_address1",
                    "shipping_street_address2",
                    "shipping_city",
                    "shipping_postcode",
                    "shipping_country",
                )
            },
        ),
        (
            "Billing Information",
            {
                "fields": (
                    "billing_full_name",
                    "billing_phone",
                    "billing_street_address1",
                    "billing_street_address2",
                    "billing_city",
                    "billing_postcode",
                    "billing_country",
                )
            },
        ),
        ("Stripe", {"fields": ("stripe_customer_id",)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
