from django.conf import settings
from django.db import models
from products.models import Product, Size

class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True, related_name="cart_items"
    )
    # For guests, we can track a session key:
    session_key = models.CharField(max_length=40, null=True, blank=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def line_total(self):
        """Total price for this cart line = product.price * quantity."""
        return self.product.price * self.quantity
    
class Order(models.Model):
    """
    An order made by a user after checkout. 
    For a typical e-commerce flow: pending → paid → shipped → delivered...
    """
    ORDER_STATUS = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="orders"
    )
    status = models.CharField(
        max_length=20, 
        choices=ORDER_STATUS, 
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order #{self.pk} - {self.get_status_display().title()}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price_each = models.DecimalField(max_digits=10, decimal_places=2)
       # price_each is captured at time of purchase in case product's price changes later.

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) - Order {self.order.pk}"

    @property
    def line_total(self):
        return self.price_each * self.quantity

    @property
    def line_total(self):
        return self.price_each * self.quantity