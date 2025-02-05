from django.db import models
from django.utils.text import slugify

# Create your models here.

class Product(models.Model):
    class CategoryChoices(models.TextChoices):
        BIRTHDAY = "birthday", "Birthday Cakes"
        WEDDING = "wedding", "Wedding Cakes"
        CUPCAKE = "cupcake", "Cupcakes"
        CUSTOM = "custom", "Custom Orders"

    class FlavorChoices(models.TextChoices):
        CHOCOLATE = "chocolate", "Chocolate"
        VANILLA = "vanilla", "Vanilla"
        RED_VELVET = "red_velvet", "Red Velvet"
        LEMON = "lemon", "Lemon"

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=20, choices=CategoryChoices.choices, default=CategoryChoices.BIRTHDAY
    )
    flavor = models.CharField(
        max_length=20, choices=FlavorChoices.choices, blank=True
    )
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    allergen_info = models.TextField(blank=True, help_text="E.g., Contains nuts, gluten-free")
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Auto-generate slug from name"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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