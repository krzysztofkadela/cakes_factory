from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from .models import CartItem, Order, OrderItem
from products.models import Product, Size
from .forms import CustomOrderForm
from django.http import JsonResponse

# Create your views here.


def cart_add(request, product_id):
    """
    Add a product to the cart. Works for both logged-in users and guests.
    """
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))
    size_id = request.POST.get("size")
    customization = request.POST.get("customization", "").strip()

    # Retrieve or create cart session
    cart = request.session.get("cart", {})

    # Get selected size object
    size = None
    if size_id:
        size = get_object_or_404(Size, id=size_id)

    # Create unique cart key
    cart_item_key = f"{product_id}_{size_id}" if size else str(product_id)

    if cart_item_key in cart:
        cart[cart_item_key]["quantity"] += quantity
    else:
        cart[cart_item_key] = {
            "name": product.name,
            "price": float(product.price),
            "quantity": quantity,
            "size": size.name if size else "Default",
            "customization": customization if customization else "None",
            "image": product.image.url if product.image else "",
        }

    request.session["cart"] = cart
    request.session.modified = True  # ✅ This ensures the session is saved

    # ✅ AJAX Support (if request is made via JavaScript)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        total_price = sum(item["price"] * item["quantity"] for item in cart.values())
        return JsonResponse({"cart_items": len(cart), "cart_total_price": total_price})

    # ✅ Redirect for normal users
    messages.success(request, f"{quantity} x {product.name} added to cart!")
    return redirect("cart_view")

def cart_view(request):
    """
    Display cart items for both guests and logged-in users.
    """
    cart_items = []
    total_price = 0

    # ✅ If user is logged in, retrieve from database
    if request.user.is_authenticated:
        db_cart_items = CartItem.objects.filter(user=request.user)

        for item in db_cart_items:
            cart_items.append({
                "product_id": item.product.id,
                "size_id": item.size.id if item.size else None,
                "name": item.product.name,
                "image": item.product.image.url if item.product.image else None,
                "price": item.product.price,
                "quantity": item.quantity,
                "size": item.size.name if item.size else "N/A",
                "customization": "None",
                "subtotal": item.line_total,
                "update_url": reverse("cart_update", args=[item.product.id, item.size.id if item.size else 0]),
                "remove_url": reverse("cart_remove", args=[item.product.id, item.size.id if item.size else 0]),
            })
            total_price += item.line_total

    # ✅ If guest user, retrieve from session
    else:
        session_cart = request.session.get("cart", {})
        for key, item in session_cart.items():
            product_id, size_id = key.split("_") if "_" in key else (key, None)

            try:
                product = Product.objects.get(id=product_id)
                size = Size.objects.get(id=size_id) if size_id else None
            except Product.DoesNotExist:
                continue
            except Size.DoesNotExist:
                size = None

            subtotal = float(item["price"]) * int(item["quantity"])
            total_price += subtotal

            cart_items.append({
                "product_id": product.id,
                "size_id": size.id if size else None,
                "name": product.name,
                "image": product.image.url if product.image else None,
                "price": float(item["price"]),
                "quantity": item["quantity"],
                "size": size.name if size else "N/A",
                "customization": item.get("customization", "None"),
                "subtotal": subtotal,
                "update_url": reverse("cart_update", args=[product.id, size.id if size else 0]),
                "remove_url": reverse("cart_remove", args=[product.id, size.id if size else 0]),
            })

    return render(request, "orders/cart.html", {"cart": cart_items, "total_price": total_price})

# Remove item from Cart
def cart_remove(request, product_id, size_id=0):
    """
    Remove an item from the cart.
    If user is logged in, delete from database.
    If guest user, delete from session.
    """
    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(user=request.user, product_id=product_id, size_id=size_id).first()
        if cart_item:
            cart_item.delete()
            messages.success(request, "Item removed from cart.")
        else:
            messages.error(request, "Item not found in cart.")

    else:
        cart = request.session.get("cart", {})
        cart_item_key = f"{product_id}_{size_id}" if int(size_id) > 0 else str(product_id)

        if cart_item_key in cart:
            del cart[cart_item_key]
            messages.success(request, "Item removed from cart.")
        else:
            messages.error(request, "Item not found in cart.")

        request.session["cart"] = cart
        request.session.modified = True

    return redirect("cart_view")

@login_required
def checkout(request):
    """Handles checkout process for logged-in users."""
    cart_items = CartItem.objects.filter(user=request.user)

    # ✅ Merge session cart if it exists
    session_cart = request.session.get("cart", {})

    if session_cart:
        for key, item in session_cart.items():
            product_id, size_id = key.split("_") if "_" in key else (key, None)
            product = get_object_or_404(Product, id=product_id)

            # ✅ Add item to user's cart if not exists
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product=product,
                size_id=size_id if size_id else None,
                defaults={"quantity": item["quantity"]},
            )

            if not created:
                cart_item.quantity += item["quantity"]
                cart_item.save()

        # ✅ Clear session cart after merging
        request.session["cart"] = {}

    if not cart_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect("cart_view")

    # ✅ Convert CartItem objects to list format
    formatted_cart = []
    total_price = 0

    for item in cart_items:
        formatted_cart.append({
            "product_id": item.product.id,
            "name": item.product.name,  # ✅ Ensure name is fetched
            "size": item.size.name if item.size else "-",
            "quantity": item.quantity,
            "price": item.product.price,
            "subtotal": item.line_total,  # Uses @property from model
        })
        total_price += item.line_total

    return render(request, "orders/checkout.html", {
        "cart": formatted_cart,  # ✅ Send formatted cart to template
        "total_price": total_price,
    })

# Order History
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/order_history.html", {"orders": orders})

# Handle Custom Orders
@login_required
def custom_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = CustomOrderForm(request.POST)
        if form.is_valid():
            custom_message = form.cleaned_data["custom_message"]

            # Store in session (until checkout)
            cart = request.session.get("cart", {})
            if str(product_id) in cart:
                cart[str(product_id)]["custom_message"] = custom_message
            else:
                cart[str(product_id)] = {
                    "name": product.name,
                    "price": float(product.price),
                    "quantity": 1,
                    "size": "",
                    "image": product.image.url if product.image else "",
                    "custom_message": custom_message,
                }

            request.session["cart"] = cart
            messages.success(request, "Custom order added to cart!")
            return redirect("cart_view")

    else:
        form = CustomOrderForm()

    return render(request, "orders/custom_order.html", {"form": form, "product": product})

def cart_update(request, product_id, size_id=0):
    """Update the quantity of a product in the cart."""
    if "cart" not in request.session:
        request.session["cart"] = {}

    cart = request.session["cart"]

    if request.method == "POST":
        new_quantity = request.POST.get("quantity")

        if new_quantity and new_quantity.isdigit():
            new_quantity = int(new_quantity)

            # Construct the correct key including size
            cart_item_key = f"{product_id}_{size_id}" if int(size_id) > 0 else str(product_id)

            if new_quantity > 0:
                if cart_item_key in cart:
                    cart[cart_item_key]["quantity"] = new_quantity
                    messages.success(request, "Cart updated successfully!")
                else:
                    messages.error(request, "Product not found in cart!")
            else:
                if cart_item_key in cart:
                    del cart[cart_item_key]
                    messages.success(request, "Item removed from cart.")

        request.session.modified = True  # Ensure session updates

    return HttpResponseRedirect(reverse("cart_view"))

@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    """
    Merge session-based cart into database-based cart when user logs in.
    """
    cart = request.session.get("cart", {})

    for key, item in cart.items():
        product_id, size_id = key.split("_") if "_" in key else (key, None)
        product = get_object_or_404(Product, id=product_id)
        size = get_object_or_404(Size, id=size_id) if size_id else None

        cart_item, created = CartItem.objects.get_or_create(
            user=user, product=product, size=size,
            defaults={"quantity": item["quantity"], "customization": item.get("customization", "")}
        )
        if not created:
            cart_item.quantity += item["quantity"]
        cart_item.save()

    request.session["cart"] = {}  # Clear session cart after merging

@receiver(user_logged_out)
def clear_cart_on_logout(sender, request, user, **kwargs):
    """
    When user logs out, clear session-based cart.
    """
    request.session["cart"] = {}
    request.session.modified = True