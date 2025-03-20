from django.conf import settings
from .models import CartItem, Product, Size


def cart_context(request):
    """
    Provides cart item count and total price for templates.
    Handles both authenticated users and guest users with session storage.
    """

    cart_items = 0
    cart_total_price = 0.0  # ✅ Default as float
    updated_session_cart = {}  # ✅ Store only valid items

    if request.user.is_authenticated:
        # ✅ LOGGED-IN USER: Fetch cart from database
        cart_items_qs = CartItem.objects.filter(user=request.user)
        cart_items = sum(item.quantity for item in cart_items_qs)
        cart_total_price = sum(item.line_total for item in cart_items_qs)

    else:
        # ✅ GUEST USER: Use session cart
        session_cart = request.session.get("cart", {})

        for key, item in session_cart.items():
            try:
                product_id = item.get("product_id")
                quantity = int(item.get("quantity", 1))
                price = float(item.get("price", 0))

                # ✅ Ensure product exists
                product = Product.objects.get(id=product_id)

                # ✅ Get size adjustment (if any)
                size_id = item.get("size_id")
                size = Size.objects.get(id=size_id) if size_id else None
                size_adjustment = 0
                if size:
                    size_adjustment = 20 if size.name == "Large" else 40
                    if size.name not in ["Large", "X-large"]:
                        size_adjustment = 0

                # ✅ Calculate item subtotal correctly
                subtotal = (price + size_adjustment) * quantity
                cart_items += quantity
                cart_total_price += subtotal

                # ✅ Store valid items in session cart
                updated_session_cart[key] = item

            except (Product.DoesNotExist, Size.DoesNotExist, ValueError, TypeError) as e:
                print(f"⚠️ Skipping invalid cart item: {e}")  # Debug invalid items

        # ✅ Remove invalid items from session cart
        if updated_session_cart != session_cart:
            request.session["cart"] = updated_session_cart
            request.session.modified = True  # ✅ Ensure session saves changes

    return {
        "cart_items": cart_items or 0,  # ✅ Always return an integer
        "cart_total_price": f"{cart_total_price:.2f}",  # ✅ Format to 2 decimal places
    }