from django import forms
from .models import Product, Size, Category, Flavor

class ProductForm(forms.ModelForm):
    """Form for adding/editing products in the admin panel."""

    sizes = forms.ModelMultipleChoiceField(
        queryset=Size.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),  # Bootstrap checkbox styling
        required=False,
        help_text="Select available sizes."
    )

    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control", "onchange": "previewImage(event)"}),  # Image preview JS
    )

    class Meta:
        model = Product
        fields = ["name", "description", "price", "category", "flavor", "sizes", "image", "allergen_info", "available"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter product name"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Enter product description"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "Enter price (€)"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "flavor": forms.Select(attrs={"class": "form-select"}),
            "allergen_info": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "List any allergens"}),
            "available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }