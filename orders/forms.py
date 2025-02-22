import datetime
from django import forms
from django.utils import timezone
from .models import Order
import re

class CustomOrderForm(forms.Form):
    custom_message = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        label="Customization Request",
        required=True,
    )
    
class OrderFormold(forms.ModelForm):
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

        # Field placeholders
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

        # Apply Bootstrap styling and placeholders
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "placeholder": placeholders.get(field, ""),
                "class": "form-control",
            })
            self.fields[field].label = False  # Hide default labels

        # ✅ Set date picker limits
        today = timezone.localdate()
        self.fields["delivery_date"].widget = forms.DateInput(
            attrs={"type": "date", "min": today.strftime("%Y-%m-%d")}
        )

        # ✅ Ensure valid time slots are always set
        time_slots = self.get_time_slots()
        if not time_slots:  # Safety check
            time_slots = [("", "No available time slots")]

        self.fields["delivery_time"].choices = time_slots

    def clean_delivery_date(self):
        """Ensure the delivery date is in the future."""
        delivery_date = self.cleaned_data.get("delivery_date")
        today = timezone.localdate()

        if delivery_date and delivery_date < today:
            raise forms.ValidationError("Delivery date cannot be in the past.")

        return delivery_date

    def clean_delivery_timeold(self):
        """Ensure the delivery time is within store hours."""
        delivery_time = self.cleaned_data.get("delivery_time")

        # Define valid time slots (store open from 9:00 AM to 6:00 PM)
        valid_times = [datetime.time(hour, minute) for hour in range(9, 18) for minute in (0, 30)]

        if delivery_time:
            # Convert string format (HH:MM) back to time object for comparison
            try:
                delivery_time_obj = datetime.datetime.strptime(delivery_time, "%H:%M").time()
            except ValueError:
                raise forms.ValidationError("Invalid time format. Please select a valid time.")

            if delivery_time_obj not in valid_times:
                raise forms.ValidationError("Please select a valid time slot within store hours (9 AM - 6 PM).")

        return delivery_time

def clean_delivery_time(self):
    """Ensure the delivery time is within store hours."""
    delivery_time = self.cleaned_data.get("delivery_time")

    # Convert time object to string if it's a datetime.time object
    if isinstance(delivery_time, datetime.time):
        delivery_time = delivery_time.strftime("%H:%M")  # Convert time to HH:MM string

    # Define valid time slots (store open from 9:00 AM to 6:00 PM)
    valid_times = [
        datetime.time(hour, minute).strftime("%H:%M")
        for hour in range(9, 18) for minute in (0, 30)
    ]

    if delivery_time and delivery_time not in valid_times:
        raise forms.ValidationError("Please select a valid time slot within store hours (9 AM - 6 PM).")

    return delivery_time
class OrderForm(forms.ModelForm):
    """Order form with delivery date & time selection."""

    class Meta:
        model = Order
        fields = (
            "full_name", "email", "phone_number",
            "street_address1", "street_address2",
            "town_or_city", "postcode", "country", "county",
            "delivery_date", "delivery_time"  # ✅ New fields
        )

    def __init__(self, *args, **kwargs):
        """Customize form fields: placeholders, Bootstrap styling, and date limits."""
        super().__init__(*args, **kwargs)

        # Field placeholders
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

        # Apply Bootstrap styling and placeholders
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "placeholder": placeholders.get(field, ""),
                "class": "form-control",
            })
            self.fields[field].label = False  # Hide default labels

        # ✅ Ensure `get_time_slots()` exists before calling it!
        self.fields["delivery_time"].widget = forms.Select(choices=self.get_time_slots())

        # Set date picker limits
        today = timezone.localdate()
        self.fields["delivery_date"].widget = forms.DateInput(
            attrs={"type": "date", "min": today.strftime("%Y-%m-%d")}
        )

    def clean_delivery_date(self):
        """Ensure the delivery date is in the future."""
        delivery_date = self.cleaned_data.get("delivery_date")
        today = timezone.localdate()
        
        if delivery_date and delivery_date < today:
            raise forms.ValidationError("Delivery date cannot be in the past.")
        
        return delivery_date

    def clean_delivery_time(self):
        """Ensure the delivery time is within store hours."""
        delivery_time = self.cleaned_data.get("delivery_time")

        # Convert time object to string if it's a datetime.time object
        if isinstance(delivery_time, datetime.time):
            delivery_time = delivery_time.strftime("%H:%M")  # Convert time to HH:MM string

        # Define valid time slots (store open from 9:00 AM to 6:00 PM)
        valid_times = [
            datetime.time(hour, minute).strftime("%H:%M")
            for hour in range(9, 18) for minute in (0, 30)
        ]

        if delivery_time and delivery_time not in valid_times:
            raise forms.ValidationError("Please select a valid time slot within store hours (9 AM - 6 PM).")

        return delivery_time

    @staticmethod
    def get_time_slots():
        """✅ Generate half-hourly time slots from 9 AM to 6 PM."""
        time_slots = [
            (datetime.time(hour, minute).strftime("%H:%M"), datetime.time(hour, minute).strftime("%I:%M %p"))
            for hour in range(9, 18) for minute in (0, 30)
        ]
        return [("", "Select Time Slot")] + time_slots  # Include a default option

@staticmethod
def get_time_slotsold():
    """Generate half-hourly time slots from 9 AM to 6 PM."""
    time_slots = [
        (datetime.time(hour, minute).strftime("%H:%M"), datetime.time(hour, minute).strftime("%I:%M %p"))
        for hour in range(9, 18) for minute in (0, 30)
    ]
    return time_slots if time_slots else [("", "No available time slots")]  # ✅ Always returns a valid list
    