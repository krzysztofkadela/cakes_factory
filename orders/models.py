import uuid
from django.conf import settings
from django.db import models
from django.db.models import Sum, F
from products.models import Product, Size

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
        base_price = self.product.price
        if self.size:
            size_multiplier = 20 * (self.size.id)  # Assuming ID 1=Small, 2=Medium, 3=Large
            return base_price + size_multiplier
        return base_price

    @property
    def line_total(self):
        """Total price for this cart item (quantity included)."""
        return self.adjusted_price * self.quantity


class Order(models.Model):
    ORDER_STATUS = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    order_number = models.CharField(max_length=32, null=False, editable=False, unique=True)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    # Order status
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        default="pending"
    )

    # Pricing fields
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def _generate_order_number(self):
        """Generate a unique order number using UUID."""
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """Update order total when items are added or removed."""
        self.order_total = self.items.aggregate(
            total=Sum(F("quantity") * F("price_each"))
        )["total"] or 0  # Avoid None values

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
        """Calculate and store price based on size selection."""
        base_price = self.product.price
        if self.size:
            size_multiplier = 20 * (self.size.id)
            return base_price + size_multiplier
        return base_price

    @property
    def line_total(self):
        return self.price_each * self.quantity

    def save(self, *args, **kwargs):
        """Ensure price_each is correctly set when saving."""
        if not self.price_each:
            self.price_each = self.adjusted_price
        super().save(*args, **kwargs)
        self.order.update_total()

    def delete(self, *args, **kwargs):
        """Update order total on item removal."""
        super().delete(*args, **kwargs)
        self.order.update_total()

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) - Order {self.order.order_number}"
