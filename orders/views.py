import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
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
from .forms import CustomOrderForm, OrderForm
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

def cart_addold(request, product_id):
    """
    Add a product to the cart with the correct size-based pricing.
    """
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))
    size_id = request.POST.get("size")
    customization = request.POST.get("customization", "").strip()

    size = Size.objects.filter(id=size_id).first() if size_id else None

    if request.user.is_authenticated:
        # ✅ LOGGED-IN USER: Use database cart
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            size=size,
            defaults={"quantity": quantity, "customization": customization}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

    else:
        # ✅ GUEST USER: Store in session
        cart = request.session.get("cart", {})
        cart_item_key = f"{product_id}_{size_id}" if size else str(product_id)

        adjusted_price = product.price
        if size:
            if size.name.lower() == "large":
                adjusted_price += 20
            elif size.name.lower() == "x-large":
                adjusted_price += 40

        if cart_item_key in cart:
            cart[cart_item_key]["quantity"] += quantity
        else:
            cart[cart_item_key] = {
                "name": product.name,
                "price": adjusted_price,
                "quantity": quantity,
                "size": size.name if size else "Default",
                "customization": customization if customization else "None",
                "image": product.image.url if product.image else "",
            }

        request.session["cart"] = cart
        request.session.modified = True  # ✅ Ensure session updates

    # ✅ AJAX Support
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_total_price = sum(float(item["price"]) * item["quantity"] for item in request.session.get("cart", {}).values())
        return JsonResponse({"cart_items": len(request.session.get("cart", {})), "cart_total_price": cart_total_price})

    messages.success(request, f"{quantity} x {product.name} added to cart!")
    return redirect("cart_view")

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))
    size_id = request.POST.get("size")
    customization = request.POST.get("customization", "").strip()

    size = Size.objects.filter(id=size_id).first() if size_id else None

    if request.user.is_authenticated:
        # LOGGED-IN USER: Use database cart
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            size=size,
            defaults={"quantity": quantity, "customization": customization}
        )
        if not created:
            cart_item.quantity += quantity
        cart_item.save()

    else:
        # GUEST USER: Store in session
        cart = request.session.get("cart", {})
        cart_item_key = f"{product_id}_{size_id}" if size else str(product_id)

        # adjusted_price likely a Decimal => cast to float
        adjusted_price = product.price
        if size:
            if size.name.lower() == "large":
                adjusted_price += 20
            elif size.name.lower() == "x-large":
                adjusted_price += 40

        adjusted_price = float(adjusted_price)  # <-- critical fix here

        if cart_item_key in cart:
            cart[cart_item_key]["quantity"] += quantity
        else:
            cart[cart_item_key] = {
                "name": product.name,
                "price": adjusted_price,  # store float
                "quantity": quantity,
                "size": size.name if size else "Default",
                "customization": customization if customization else "None",
                "image": product.image.url if product.image else "",
            }

        request.session["cart"] = cart
        request.session.modified = True

    # AJAX support
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Convert any potential decimals to float again
        cart_total_price = sum(
            float(item["price"]) * item["quantity"]
            for item in request.session.get("cart", {}).values()
        )
        return JsonResponse({
            "cart_items": len(request.session.get("cart", {})),
            "cart_total_price": float(cart_total_price),
        })

    messages.success(request, f"{quantity} x {product.name} added to cart!")
    return redirect("cart_view")

def cart_view(request):
    """
    Display cart items for both guests and logged-in users.
    """
    cart_items = []
    total_price = 0

    if request.user.is_authenticated:
        # ✅ LOGGED-IN USERS: Fetch cart from DB
        db_cart_items = CartItem.objects.filter(user=request.user)

        for item in db_cart_items:
            adjusted_price = item.adjusted_price  # ✅ Adjusted price for size
            subtotal = adjusted_price * item.quantity
            total_price += subtotal

            cart_items.append({
                "product_id": item.product.id,
                "size_id": item.size.id if item.size else None,
                "name": item.product.name,
                "image": item.product.image.url if item.product.image else None,
                "price": adjusted_price,
                "quantity": item.quantity,
                "size": item.size.name if item.size else "N/A",
                "customization": item.customization if item.customization else "None",
                "subtotal": subtotal,
                "update_url": reverse("cart_update", args=[item.product.id, item.size.id if item.size else 0]),
                "remove_url": reverse("cart_remove", args=[item.product.id, item.size.id if item.size else 0]),
            })

    else:
        # ✅ GUEST USERS: Fetch from session
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

def checkout(request):
    """
    Checkout view for both guests and logged-in users.
    We separate the logic to avoid mixing bracket-notation
    (for session cart) with dot-notation (for CartItem objects).
    """

    # --------------------------
    # 1. Build a list of cart items
    #    as dictionaries for uniformity
    # --------------------------
    cart_list = []
    total_price = 0

    if request.user.is_authenticated:
        # Auth user: get cart from DB
        db_cart_items = CartItem.objects.filter(user=request.user)

        if not db_cart_items.exists():
            messages.error(request, "Your cart is empty!")
            return redirect("cart_view")

        # Convert db CartItem objects to dictionaries
        for item in db_cart_items:
            line_subtotal = float(item.line_total)
            total_price += line_subtotal

            cart_list.append({
                "product": item.product,
                "size": item.size,
                "quantity": item.quantity,
                "price": float(item.adjusted_price),  # Convert Decimal to float
                "subtotal": line_subtotal,
            })
    else:
        # Guest user: get cart from session
        session_cart = request.session.get("cart", {})
        if not session_cart:
            messages.error(request, "Your cart is empty!")
            return redirect("cart_view")

        for key, val in session_cart.items():
            product_id, size_id = key.split("_") if "_" in key else (key, None)
            try:
                product = Product.objects.get(id=product_id)
                size = Size.objects.get(id=size_id) if size_id else None

                quantity = val["quantity"]
                price = float(val["price"])
                subtotal = price * quantity
                total_price += subtotal

                cart_list.append({
                    "product": product,
                    "size": size,
                    "quantity": quantity,
                    "price": price,
                    "subtotal": subtotal,
                })

            except (Product.DoesNotExist, Size.DoesNotExist):
                continue

    # --------------------------
    # 2. Handle POST: place order
    # --------------------------
    if request.method == "POST":
        form = OrderForm(request.POST)
        create_account = request.POST.get("create_account")

        if form.is_valid():
            # Create the Order object from the form
            new_order = form.save(commit=False)
            if request.user.is_authenticated:
                new_order.user = request.user
            new_order.save()

            # Create OrderItems from our cart_list
            for c_item in cart_list:
                OrderItem.objects.create(
                    order=new_order,
                    product=c_item["product"],
                    size=c_item["size"],
                    quantity=c_item["quantity"],
                    price_each=c_item["price"]
                )

            # If guest wants to create an account
            if not request.user.is_authenticated and create_account:
                email = form.cleaned_data['email']
                if not User.objects.filter(username=email).exists():
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password="temporarypassword"
                    )
                    new_order.user = user
                    new_order.save()
                    messages.success(request, "Account created! Check your email to set a password.")

            # Clear the cart
            if request.user.is_authenticated:
                CartItem.objects.filter(user=request.user).delete()
            else:
                request.session["cart"] = {}
                request.session.modified = True

            messages.success(request, "Order placed! Proceed to payment.")
            return redirect("some_payment_view")  # Replace with your payment step

        else:
            messages.error(request, "Please correct the errors in the form.")
    
    else:
        # Pre-fill form for logged-in users
        initial_data = {}
        if request.user.is_authenticated:
            initial_data["full_name"] = request.user.get_full_name()
            initial_data["email"] = request.user.email
        form = OrderForm(initial=initial_data)

    return render(request, "orders/checkout.html", {
        "form": form,
        "cart_items": cart_list,   # a list of dicts
        "total_price": total_price,
    })

def checkoutold(request):
    """Handles checkout process for logged-in users."""
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect("cart_view")

    formatted_cart = []
    total_price = 0

    for item in cart_items:
        adjusted_price = item.adjusted_price  # ✅ Corrected price calculation
        subtotal = adjusted_price * item.quantity

        formatted_cart.append({
            "product_id": item.product.id,
            "name": item.product.name,
            "size": item.size.name if item.size else "-",
            "quantity": item.quantity,
            "price": adjusted_price,
            "subtotal": subtotal,
        })
        total_price += subtotal

    return render(request, "orders/checkout.html", {
        "cart": formatted_cart,
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
    """Update the quantity of a product in the cart for both guests & logged-in users."""
    new_quantity = request.POST.get("quantity")

    if not new_quantity or not new_quantity.isdigit():
        messages.error(request, "Invalid quantity.")
        return HttpResponseRedirect(reverse("cart_view"))

    new_quantity = int(new_quantity)

    if request.user.is_authenticated:
        # ✅ LOGGED-IN USERS: Update in database
        cart_item = CartItem.objects.filter(
            user=request.user, product_id=product_id, size_id=size_id if size_id else None
        ).first()

        if cart_item:
            if new_quantity > 0:
                cart_item.quantity = new_quantity
                cart_item.save()
                messages.success(request, "Cart updated successfully!")
            else:
                cart_item.delete()
                messages.success(request, "Item removed from cart.")
        else:
            messages.error(request, "Item not found in cart.")

    else:
        # ✅ GUEST USERS: Update session cart
        cart = request.session.get("cart", {})
        cart_item_key = f"{product_id}_{size_id}" if int(size_id) > 0 else str(product_id)

        if cart_item_key in cart:
            if new_quantity > 0:
                cart[cart_item_key]["quantity"] = new_quantity
                messages.success(request, "Cart updated successfully!")
            else:
                del cart[cart_item_key]
                messages.success(request, "Item removed from cart.")
        else:
            messages.error(request, "Item not found in cart.")

        request.session["cart"] = cart
        request.session.modified = True  # ✅ Ensure session is updated

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

@login_required
def create_checkout_session(request):
    """
    1. Gather the user's cart items and total.
    2. Create a Stripe Checkout Session.
    3. Redirect user to the session's URL.
    """
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    
    if not cart_items.exists():
        # no items in cart, handle error or redirect
        return redirect("cart_view")
    
    # Build line items array for Stripe
    # We'll show a simple example with quantity & price each item
    line_items = []
    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'eur',  # or 'usd', etc.
                'product_data': {
                    'name': item.product.name,
                },
                'unit_amount': int(item.adjusted_price * 100),  # in cents
            },
            'quantity': item.quantity,
        })

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],  # or more
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri('/payment/success/'),
            cancel_url=request.build_absolute_uri('/payment/cancel/'),
        )
        
        # Stripe responds with a session object that includes a URL
        return redirect(checkout_session.url)

    except Exception as e:
        # Handle error properly in production
        return JsonResponse({'error': str(e)})
    

def payment_success(request):
    # Clear user cart or mark items as purchased
    # Show a success message
    return render(request, 'payment_success.html')

def payment_cancel(request):
    # Just show a "Payment canceled" message, let them retry
    return render(request, 'payment_cancel.html')