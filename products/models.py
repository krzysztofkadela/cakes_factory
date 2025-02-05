from django.db import models

# Create your models here.

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('birthday', 'Birthday Cakes'),
        ('wedding', 'Wedding Cakes'),
        ('cupcake', 'Cupcakes'),
        ('custom', 'Custom Orders'),
    ]

    FLAVOR_CHOICES = [
        ('chocolate', 'Chocolate'),
        ('vanilla', 'Vanilla'),
        ('red_velvet', 'Red Velvet'),
        ('lemon', 'Lemon'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    flavor = models.CharField(max_length=20, choices=FLAVOR_CHOICES, blank=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    available_dates = models.JSONField(default=list, help_text="Available delivery/pickup dates")
    allergen_info = models.TextField(blank=True, help_text="E.g., Contains nuts, gluten-free")
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    # Review model for customer review and rating

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product.name} ({self.rating}/5)"  