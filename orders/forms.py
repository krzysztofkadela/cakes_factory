from django import forms
from .models import Order
import re

class CustomOrderForm(forms.Form):
    custom_message = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        label="Customization Request",
        required=True,
    )
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "full_name", "email", "phone_number",
            "street_address1", "street_address2",
            "town_or_city", "postcode", "country",
            "county"
        )

    def __init__(self, *args, **kwargs):
        """
        Customize form fields: add placeholders, remove labels, and set autofocus.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            "full_name": "Full Name",
            "email": "Email Address",
            "phone_number": "Phone Number",
            "country": "Country",
            "postcode": "Postal Code",
            "town_or_city": "Town or City",
            "street_address1": "Street Address 1",
            "street_address2": "Street Address 2",
            "county": "County",
        }

        self.fields["full_name"].widget.attrs["autofocus"] = True
        for field in self.fields:
            placeholder = f"{placeholders[field]} *" if self.fields[field].required else placeholders[field]
            self.fields[field].widget.attrs.update({
                "placeholder": placeholder,
                "class": "form-control",  # ✅ Bootstrap styling
            })
            self.fields[field].label = False  # Hide default labels

    def clean_email(self):
        """Ensure email format is valid."""
        email = self.cleaned_data.get("email")
        if email and "@" not in email:
            raise forms.ValidationError("Please enter a valid email address.")
        return email

    def clean_phone_number(self):
        """Ensure phone number is in a valid format (digits only, optional + at start)."""
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not re.match(r"^\+?\d{7,15}$", phone_number):
            raise forms.ValidationError("Enter a valid phone number (7-15 digits).")
        return phone_number

    def clean_postcode(self):
        """Ensure postcode is entered."""
        postcode = self.cleaned_data.get("postcode")
        if not postcode:
            raise forms.ValidationError("Please enter your postal code.")
        return postcode