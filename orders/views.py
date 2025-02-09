from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from products.models import Product

# Create your views here.

# Add Product to Cart (Session-based cart)
@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {})

    # Get quantity from request
    quantity = int(request.POST.get("quantity", 1))
    size = request.POST.get("size", "")

    if str(product_id) in cart:
        cart[str(product_id)]["quantity"] += quantity
    else:
        cart[str(product_id)] = {
            "name": product.name,
            "price": float(product.price),
            "quantity": quantity,
            "size": size,
            "image": product.image.url if product.image else "",
        }

    request.session["cart"] = cart
    messages.success(request, f"{product.name} added to cart!")
    return redirect("cart_view")