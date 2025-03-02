from django import forms
from .models import Product, Size

class ProductForm(forms.ModelForm):
    """Form for adding/editing products in the admin panel."""

    sizes = forms.ModelMultipleChoiceField(
        queryset=Size.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select available sizes."
    )

    class Meta:
        model = Product
        fields = ["name", "description", "price", "category", "flavor", "sizes", "image", "allergen_info", "available"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "flavor": forms.Select(attrs={"class": "form-select"}),
            "allergen_info": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }