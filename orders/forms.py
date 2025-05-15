import datetime
from django import forms
from django.utils import timezone
from .models import Order


class CustomOrderForm(forms.Form):
    custom_message = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        label="Customization Request",
        required=True,
    )


class OrderForm(forms.ModelForm):
    """Order form with shipping & billing fields, plus delivery date/time."""

    use_same_for_billing = forms.BooleanField(
        required=False,
        initial=True,  # By default, assume billing is the same as shipping
        label="Billing address is the same as shipping",
    )

    class Meta:
        model = Order
        fields = (
            # Shipping fields
            "full_name",
            "email",
            "phone_number",
            "street_address1",
            "street_address2",
            "town_or_city",
            "county",
            "postcode",
            "country",
            # Delivery date/time
            "delivery_date",
            "delivery_time",
            # Billing fields
            "billing_full_name",
            "billing_phone_number",
            "billing_street_address1",
            "billing_street_address2",
            "billing_town_or_city",
            "billing_county",
            "billing_postcode",
            "billing_country",
        )

    def __init__(self, *args, **kwargs):
        """Customize form fields: placeholders,
        Bootstrap styling, and date limits.
        """
        super().__init__(*args, **kwargs)

        # Placeholder text for shipping fields
        placeholders = {
            "full_name": "Full Name (Shipping)",
            "email": "Email Address",
            "phone_number": "Phone Number (Shipping)",
            "street_address1": "Shipping Street Address 1",
            "street_address2": "Shipping Street Address 2",
            "town_or_city": "Shipping Town or City",
            "county": "Shipping County",
            "postcode": "Shipping Postal Code",
            "country": "Shipping Country",
            "delivery_date": "Select Delivery or Pickup Date",
            "delivery_time": "Select Preferred Time Slot",
            # Billing
            "billing_full_name": "Full Name (Billing)",
            "billing_phone_number": "Phone Number (Billing)",
            "billing_street_address1": "Billing Street Address 1",
            "billing_street_address2": "Billing Street Address 2",
            "billing_town_or_city": "Billing Town or City",
            "billing_county": "Billing County",
            "billing_postcode": "Billing Postal Code",
            "billing_country": "Billing Country",
        }

        for field in self.fields:
            # Skip adding placeholder to the BooleanField
            if field == "use_same_for_billing":
                continue

            self.fields[field].widget.attrs.update(
                {
                    "placeholder": placeholders.get(field, ""),
                    "class": "form-control",
                }
            )
            self.fields[field].label = False

        # Use a select widget for delivery_time with generated time slots
        self.fields["delivery_time"].widget = forms.Select(
            choices=self.get_time_slots()
        )

        # Set date picker for delivery_date (today’s date or later)
        today = timezone.localdate()
        self.fields["delivery_date"].widget = forms.DateInput(
            attrs={"type": "date", "min": today.strftime("%Y-%m-%d")}
        )

    def clean_delivery_date(self):
        """Ensure the delivery date is not in the past."""
        delivery_date = self.cleaned_data.get("delivery_date")
        if delivery_date and delivery_date < timezone.localdate():
            raise forms.ValidationError("Delivery date cannot be in the past.")
        return delivery_date

    def clean_delivery_time(self):
        """Ensure the delivery time is within store hours (9:00-18:00)."""
        delivery_time = self.cleaned_data.get("delivery_time")
        if isinstance(delivery_time, datetime.time):
            delivery_time = delivery_time.strftime("%H:%M")

        valid_times = [
            datetime.time(hour, minute).strftime("%H:%M")
            for hour in range(9, 18)
            for minute in (0, 30)
        ]
        if delivery_time and delivery_time not in valid_times:
            raise forms.ValidationError(
                "Please select a valid time slot(9 AM - 6 PM)."
            )
        return delivery_time

    def clean(self):
        """If 'use_same_for_billing' is checked,
        copy shipping fields into billing fields.
        """
        cleaned_data = super().clean()
        use_same = cleaned_data.get("use_same_for_billing")

        if use_same:
            cleaned_data["billing_full_name"] = cleaned_data.get("full_name")
            cleaned_data["billing_phone_number"] = cleaned_data.get(
                "phone_number"
            )
            cleaned_data["billing_street_address1"] = cleaned_data.get(
                "street_address1"
            )
            cleaned_data["billing_street_address2"] = cleaned_data.get(
                "street_address2"
            )
            cleaned_data["billing_town_or_city"] = cleaned_data.get(
                "town_or_city"
            )
            cleaned_data["billing_county"] = cleaned_data.get("county")
            cleaned_data["billing_postcode"] = cleaned_data.get("postcode")
            cleaned_data["billing_country"] = cleaned_data.get("country")

        return cleaned_data

    @staticmethod
    def get_time_slots():
        """Generate half-hourly time slots from 9 AM to 6 PM."""
        time_slots = [
            (
                datetime.time(hour, minute).strftime("%H:%M"),
                datetime.time(hour, minute).strftime("%I:%M %p"),
            )
            for hour in range(9, 18)
            for minute in (0, 30)
        ]
        return [("", "Select Time Slot")] + time_slots
