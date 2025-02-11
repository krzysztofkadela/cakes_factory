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

# Create your views here.

# Add Product to Cart (Session-based for guests, DB-based for users)
def cart_add(request, product_id):
    """
    Add product to cart. Stores in session if user is a guest, 
    or in the database if logged in.
    """
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))
    size_id = request.POST.get("size")
    customization = request.POST.get("customization", "").strip()

    # If user is logged in, store in database
    if request.user.is_authenticated:
        size = Size.objects.get(id=size_id) if size_id else None
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, product=product, size=size,
            defaults={"quantity": quantity, "customization": customization}
        )
        if not created:
            cart_item.quantity += quantity
        cart_item.save()

    # If user is not logged in, store in session
    else:
        cart = request.session.get("cart", {})

        size_name = size.name if (size := Size.objects.get(id=size_id)) else "Default"
        cart_item_key = f"{product_id}_{size_id}" if size_id else str(product_id)

        if cart_item_key in cart:
            cart[cart_item_key]["quantity"] += quantity
        else:
            cart[cart_item_key] = {
                "name": product.name,
                "price": float(product.price),
                "quantity": quantity,
                "size": size_name,
                "customization": customization if customization else "None",
                "image": product.image.url if product.image else "",
            }

        request.session["cart"] = cart
        request.session.modified = True

    messages.success(request, f"{quantity} x {product.name} added to cart!")
    return redirect("cart_view")

# View Cart
def cart_view(request):
    """
    Display cart items, combining session-based and database-based cart.
    """
    cart_items = []

    # If user is logged in, retrieve from database
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)

    # If guest user, retrieve from session
    else:
        session_cart = request.session.get("cart", {})
        for key, item in session_cart.items():
            product_id, size_id = key.split("_") if "_" in key else (key, None)
            cart_items.append({
                "product_id": product_id,
                "name": item["name"],
                "price": item["price"],
                "quantity": item["quantity"],
                "size": item["size"],
                "customization": item["customization"],
                "subtotal": float(item["price"]) * int(item["quantity"]),
                "remove_url": reverse("cart_remove", args=[product_id, size_id or 0]),
            })

    total_price = sum(item["subtotal"] if isinstance(item, dict) else item.line_total for item in cart_items)

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

# Checkout Process
@login_required
def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect("cart_view")

    if request.method == "POST":
        order = Order.objects.create(user=request.user, total_price=0)
        total_price = 0

        for product_id, item in cart.items():
            product = get_object_or_404(Product, id=product_id)
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item["quantity"],
                size=item["size"],
                price=item["price"],
            )
            total_price += item["price"] * item["quantity"]

        order.total_price = total_price
        order.save()

        request.session["cart"] = {}  # Clear cart after checkout
        messages.success(request, "Your order has been placed!")
        return redirect("order_history")

    return render(request, "orders/checkout.html", {"cart": cart})

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