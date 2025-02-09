from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from products.models import Product, Size
from .forms import CustomOrderForm

# Create your views here.

# Add Product to Cart (Session-based cart)
@login_required
def cart_add(request, product_id):
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

    # Store product with size & customization
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
    messages.success(request, f"{quantity} x {product.name} ({size.name if size else 'Default'}) added to cart!")
    return redirect("cart_view")

# View Cart
@login_required
def cart_view(request):
    cart = request.session.get("cart", {})
    total_price = 0  # Store total cost

    for key, item in cart.items():
        product_id, size_id = key.split("_") if "_" in key else (key, None)

        # Calculate subtotal
        item["subtotal"] = float(item["price"]) * int(item["quantity"])

        # Add to total price
        total_price += item["subtotal"]

        # Generate remove URL
        item["remove_url"] = reverse("cart_remove", args=[product_id, size_id or 0])

    return render(request, "orders/cart.html", {"cart": cart, "total_price": total_price})

# Remove item from Cart
@login_required
def cart_remove(request, product_id, size_id=0):
    cart = request.session.get("cart", {})

    # Construct the correct key
    cart_item_key = f"{product_id}_{size_id}" if int(size_id) > 0 else str(product_id)

    if cart_item_key in cart:
        del cart[cart_item_key]
        messages.success(request, "Item removed from cart.")
    else:
        messages.error(request, "Item not found in cart.")

    request.session["cart"] = cart
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