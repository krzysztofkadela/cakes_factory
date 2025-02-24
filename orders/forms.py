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
    """Order form with delivery date & time selection."""
    class Meta:
        model = Order
        fields = (
            "full_name", "email", "phone_number",
            "street_address1", "street_address2",
            "town_or_city", "postcode", "country", "county",
            "delivery_date", "delivery_time"
        )

    def __init__(self, *args, **kwargs):
        """Customize form fields: placeholders, Bootstrap styling, and date limits."""
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
            "delivery_date": "Select Delivery or Pickup Date",
            "delivery_time": "Select Preferred Time Slot",
        }
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "placeholder": placeholders.get(field, ""),
                "class": "form-control",
            })
            self.fields[field].label = False

        # Use a select widget for delivery_time with generated time slots
        self.fields["delivery_time"].widget = forms.Select(choices=self.get_time_slots())

        # Set date picker limits (today’s date or later)
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
            for hour in range(9, 18) for minute in (0, 30)
        ]
        if delivery_time and delivery_time not in valid_times:
            raise forms.ValidationError("Please select a valid time slot within store hours (9 AM - 6 PM).")
        return delivery_time

    @staticmethod
    def get_time_slots():
        """Generate half-hourly time slots from 9 AM to 6 PM."""
        time_slots = [
            (datetime.time(hour, minute).strftime("%H:%M"), datetime.time(hour, minute).strftime("%I:%M %p"))
            for hour in range(9, 18) for minute in (0, 30)
        ]
        return [("", "Select Time Slot")] + time_slots