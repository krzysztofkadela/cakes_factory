from .models import CartItem
from django.conf import settings

def cart_context(request):
    cart_items = 0
    cart_total_price = 0.0

    if request.user.is_authenticated:
        # ✅ LOGGED-IN USER: Use database cart
        cart_items_qs = CartItem.objects.filter(user=request.user)
        cart_items = sum(item.quantity for item in cart_items_qs)
        cart_total_price = sum(item.line_total for item in cart_items_qs)
    else:
        # ✅ GUEST USER: Use session cart
        session_cart = request.session.get("cart", {})
        cart_items = sum(item["quantity"] for item in session_cart.values())
        cart_total_price = sum(float(item["price"]) * int(item["quantity"]) for item in session_cart.values())

    return {"cart_items": cart_items, "cart_total_price": cart_total_price}