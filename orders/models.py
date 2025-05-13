import uuid
import stripe
from django.db import models
from django.conf import settings
from django.db.models import Sum, F
from django.urls import reverse
from products.models import Product, Size

stripe.api_key = settings.STRIPE_SECRET_KEY


class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True, related_name="cart_items"
    )
    session_key = models.CharField(
        max_length=40, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(
        Size, on_delete=models.SET_NULL, null=True, blank=True)
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
        base_price = self.product.price or 0
        size_adjustment = SIZE_PRICE_ADJUSTMENT.get(
            self.size.name if self.size else "Small", 0)
        return base_price + size_adjustment

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
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )

    order_number = models.CharField(
        max_length=32, null=False, editable=False, unique=True)

    # Shipping Fields
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=40)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40)
    street_address1 = models.CharField(max_length=80)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)

    # Billing Fields
    billing_full_name = models.CharField(
        max_length=50, blank=True, null=True)
    billing_phone_number = models.CharField(
        max_length=20, blank=True, null=True)
    billing_country = models.CharField(
        max_length=40, blank=True, null=True)
    billing_postcode = models.CharField(
        max_length=20, blank=True, null=True)
    billing_town_or_city = models.CharField(
        max_length=40, blank=True, null=True)
    billing_street_address1 = models.CharField(
        max_length=80, blank=True, null=True)
    billing_street_address2 = models.CharField(
        max_length=80, blank=True, null=True)
    billing_county = models.CharField(
        max_length=80, blank=True, null=True)

    # Delivery/Pickup Date & Time
    delivery_date = models.DateField(null=True, blank=True)
    delivery_time = models.TimeField(null=True, blank=True)

    date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        default="pending"
    )

    # Pricing Fields
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, default=0)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    def _generate_order_number(self):
        """Generate a unique order number using UUID."""
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """ Fixed: Update order total properly from OrderItem prices."""
        self.order_total = self.items.aggregate(
            total=Sum(F("quantity") * F("price_each")))["total"] or 0

        # If the order total is below FREE_DELIVERY_THRESHOLD
        #  apply delivery cost
        self.delivery_cost = 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = settings.STANDARD_DELIVERY_CHARGE

        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """Ensure order number is generated before saving."""
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def get_stripe_checkout_url(self):
        """Improved: Generate a Stripe Checkout URL for retrying payment."""
        if self.status == "paid":
            return None  # No need to retry if the order is already paid

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                mode="payment",
                line_items=[{
                    "price_data": {
                        "currency": "eur",
                        "product_data": {"name": f"Order {self.order_number}"},
                        # Convert to cents
                        "unit_amount": int(self.grand_total * 100),
                    },
                    "quantity": 1,
                }],
                metadata={"order_number": self.order_number},
                success_url=f"{settings.SITE_URL}{reverse('payment_success')}",
                cancel_url=f"{settings.SITE_URL}{reverse(
                    'order_detail', args=[self.order_number])}",
            )
            return session.url
        except Exception as e:
            print(f"❌ Stripe Error: {e}")
            return None

    def __str__(self):
        return f"Order #{self.order_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(
        Size, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price_each = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def line_total(self):
        """Ensure order item total calculation is safe even if price_each is None."""
        price = self.price_each or 0
        quantity = self.quantity or 0
        return price * quantity

    def save(self, *args, **kwargs):
        """Ensure price_each is correctly set before saving."""
        super().save(*args, **kwargs)
        self.order.update_total()  # Update order total

    def delete(self, *args, **kwargs):
        """Update order total on item removal."""
        super().delete(*args, **kwargs)
        self.order.update_total()

    def __str__(self):
        return (f"{self.product.name} ({self.quantity}) - "
                f"Order {self.order.order_number}")
