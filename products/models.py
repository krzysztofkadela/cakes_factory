from django.db import models
from django.utils.text import slugify

class Size(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Flavor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="products"
    )
    flavor = models.ForeignKey(
        Flavor, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="products"
    )
    sizes = models.ManyToManyField(
        Size, blank=True, related_name="products"
    )

    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    allergen_info = models.TextField(blank=True, help_text="E.g., Contains nuts, gluten-free")
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # ✅ Generate slug if missing
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)  # Save product first

        # ✅ Ensure at least one default size is assigned
        if not self.sizes.exists():
            default_size, created = Size.objects.get_or_create(
                name="Standard", defaults={"slug": slugify("Standard")}
            )
            self.sizes.add(default_size)  # Assign "Standard" size

    def __str__(self):
        return self.name


class Review(models.Model):
    """Customer review and rating for a product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product.name} ({self.rating}/5)"