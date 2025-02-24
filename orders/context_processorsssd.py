from .models import CartItem, Product, Size
from django.conf import settings

def cart_contextold(request):
    cart_items = 0
    cart_total_price = 0.0

    if request.user.is_authenticated:
        # ✅ LOGGED-IN USER: Fetch cart from the database
        cart_items_qs = CartItem.objects.filter(user=request.user)
        cart_items = sum(item.quantity for item in cart_items_qs)
        cart_total_price = sum(item.line_total for item in cart_items_qs)  # ✅ Uses line_total for correct pricing
    else:
        # ✅ GUEST USER: Use session cart
        session_cart = request.session.get("cart", {})

        for item in session_cart.values():
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
                if size and size.name in ["Large", "X-large"]:
                    size_adjustment = 20 if size.name == "Large" else 40

                # ✅ Calculate item subtotal
                subtotal = (price + size_adjustment) * quantity
                cart_items += quantity
                cart_total_price += subtotal

            except (Product.DoesNotExist, Size.DoesNotExist, ValueError, TypeError):
                continue  # Skip invalid cart items to prevent errors

    return {
        "cart_items": cart_items or 0,  # ✅ Always return an integer
        "cart_total_price": round(cart_total_price, 2)  # ✅ Ensure two decimal places
    }

def cart_context(request):
    cart_items = 0
    cart_total_price = 0.0  # ✅ Default to float
    updated_session_cart = {}  # ✅ Store valid items only

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
                if size and size.name == "Large":
                    size_adjustment = 20
                elif size and size.name == "X-large":
                    size_adjustment = 40

                # ✅ Calculate item subtotal correctly
                subtotal = (price + size_adjustment) * quantity
                cart_items += quantity
                cart_total_price += subtotal

                # ✅ Store valid items in session cart
                updated_session_cart[key] = item

            except (Product.DoesNotExist, Size.DoesNotExist, ValueError, TypeError) as e:
                print(f"⚠️ Skipping invalid cart item: {e}")  # Debugging invalid items

        # ✅ Update session cart to remove invalid items
        if updated_session_cart != session_cart:
            request.session["cart"] = updated_session_cart
            request.session.modified = True  # ✅ Ensure session saves changes

    return {
        "cart_items": cart_items or 0,  # ✅ Always return an integer
        "cart_total_price": f"{cart_total_price:.2f}"  # ✅ Format to 2 decimal places
    }