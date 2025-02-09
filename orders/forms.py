from django import forms

class CustomOrderForm(forms.Form):
    custom_message = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        label="Customization Request",
        required=True,
    )