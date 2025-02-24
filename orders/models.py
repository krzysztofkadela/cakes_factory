import uuid
from django.conf import settings
from django.db import models
from django.db.models import Sum, F
from products.models import Product, Size
from django.contrib.auth.models import User

class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True, related_name="cart_items"
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)  # For guest users
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    customization = models.TextField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def adjusted_price(self):
        """Calculate price based on size selection."""
        SIZE_PRICE_ADJUSTMENT = {
            "Small": 0,  
            "Large": 20,  
            "X-large": 40  
        }
        # Assume product.price is always set; fallback is provided just in case.
        base_price = self.product.price or 0
        size_adjustment = SIZE_PRICE_ADJUSTMENT.get(self.size.name if self.size else "Small", 0)
        return base_price + size_adjustment

    @property
    def line_total(self):
        """Total price for this cart item (quantity included)."""
        # If adjusted_price somehow is None, fallback to 0.
        return (self.adjusted_price or 0) * self.quantity


class Order(models.Model):
    ORDER_STATUS = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )

    order_number = models.CharField(max_length=32, null=False, editable=False, unique=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=40)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40)
    street_address1 = models.CharField(max_length=80)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    # Delivery/Pickup Date & Time
    delivery_date = models.DateField(null=True, blank=True)
    delivery_time = models.TimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        default="pending"
    )

    # Pricing fields
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def _generate_order_number(self):
        """Generate a unique order number using UUID."""
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """Update order total when items are added or removed."""
        self.order_total = self.items.aggregate(
            total=Sum(F("quantity") * F("price_each"))
        )["total"] or 0

        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * (settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        else:
            self.delivery_cost = 0

        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """Ensure order number is generated before saving."""
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price_each = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def adjusted_price(self):
        """Calculate price based on size selection."""
        SIZE_PRICE_ADJUSTMENT = {
            "Small": 0,  
            "Large": 20,  
            "X-large": 40 
        }
        base_price = self.product.price or 0
        size_adjustment = SIZE_PRICE_ADJUSTMENT.get(self.size.name if self.size else "Small", 0)
        return base_price + size_adjustment

    @property
    def line_total(self):
        # Use a fallback value (0) if price_each is None.
        return (self.price_each or 0) * self.quantity

    def save(self, *args, **kwargs):
        """Ensure price_each is correctly set before saving."""
        self.price_each = self.adjusted_price
        super().save(*args, **kwargs)
        self.order.update_total()

    def delete(self, *args, **kwargs):
        """Update order total on item removal."""
        super().delete(*args, **kwargs)
        self.order.update_total()

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) - Order {self.order.order_number}"