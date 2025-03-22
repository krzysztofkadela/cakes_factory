# users/forms.py
from django import forms
from .models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            # Core fields
            'first_name', 'last_name', 'email',
            # Shipping
            'shipping_full_name', 'shipping_phone', 'shipping_street_address1',
            'shipping_street_address2', 'shipping_city', 'shipping_postcode',
            'shipping_country',
            # Billing
            'billing_full_name', 'billing_phone', 'billing_street_address1',
            'billing_street_address2', 'billing_city', 'billing_postcode',
            'billing_country',
        ]
        # labels to prettify the form
        labels = {
            'shipping_full_name': "Full Name (Shipping)",
            'billing_full_name': "Full Name (Billing)",
            # etc...
        }
        widgets = {
            'shipping_full_name':
                forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_phone': forms.TextInput(attrs={'class': 'form-control'}),
            # Add similar widget settings for all fields...
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username", "email", "first_name", "last_name",
            "is_active", "is_staff", "is_superuser"
        ]
