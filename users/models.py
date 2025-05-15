from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField


class CustomUser(AbstractUser):
    """Custom user model extending Django's built-in User."""

    stripe_customer_id = models.CharField(
        max_length=50, blank=True, null=True, unique=True
    )

    # Shipping Address
    shipping_full_name = models.CharField(
        max_length=100, blank=True, null=True
    )
    shipping_phone = models.CharField(max_length=20, blank=True, null=True)
    shipping_street_address1 = models.CharField(
        max_length=255, blank=True, null=True
    )
    shipping_street_address2 = models.CharField(
        max_length=255, blank=True, null=True
    )
    shipping_city = models.CharField(max_length=100, blank=True, null=True)
    shipping_postcode = models.CharField(max_length=20, blank=True, null=True)
    shipping_country = CountryField(
        blank_label="Select country", blank=True, null=True
    )

    # Billing Address
    billing_full_name = models.CharField(max_length=100, blank=True, null=True)
    billing_phone = models.CharField(max_length=20, blank=True, null=True)
    billing_street_address1 = models.CharField(
        max_length=255, blank=True, null=True
    )
    billing_street_address2 = models.CharField(
        max_length=255, blank=True, null=True
    )
    billing_city = models.CharField(max_length=100, blank=True, null=True)
    billing_postcode = models.CharField(max_length=20, blank=True, null=True)
    billing_country = CountryField(
        blank_label="Select country", blank=True, null=True
    )

    def __str__(self):
        return self.username
