from django.conf import settings
from .models import CartItem


def cart_context(request):
    """Provides cart item count and total price across all templates."""

    cart_items = 0
    cart_total_price = 0.0

    if request.user.is_authenticated:
        # LOGGED-IN USER: Retrieve cart from database
        cart_items_qs = CartItem.objects.filter(user=request.user)
        cart_items = sum(item.quantity for item in cart_items_qs)
        cart_total_price = sum(item.line_total for item in cart_items_qs)
    else:
        # GUEST USER: Retrieve cart from session
        session_cart = request.session.get("cart", {})
        cart_items = sum(item["quantity"] for item in session_cart.values())
        cart_total_price = sum(
            float(item["price"]) * int(item["quantity"])
            for item in session_cart.values()
        )

    return {
        "cart_items": cart_items,
        "cart_total_price": cart_total_price,
    }
