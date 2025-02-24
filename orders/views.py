import stripe
from decimal import Decimal
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import CartItem, Order, OrderItem
from .forms import CustomOrderForm, OrderForm
from products.models import Product, Size

stripe.api_key = settings.STRIPE_SECRET_KEY

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))
    size_id = request.POST.get("size")
    customization = request.POST.get("customization", "").strip()
    size = Size.objects.filter(id=size_id).first() if size_id else None

    if request.user.is_authenticated:
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
        cart = request.session.get("cart", {})
        cart_item_key = f"{product_id}_{size_id}" if size else str(product_id)
        adjusted_price = product.price
        if size:
            if size.name.lower() == "large":
                adjusted_price += 20
            elif size.name.lower() == "x-large":
                adjusted_price += 40
        adjusted_price = float(adjusted_price)
        if cart_item_key in cart:
            cart[cart_item_key]["quantity"] += quantity
        else:
            cart[cart_item_key] = {
                "name": product.name,
                "price": adjusted_price,
                "quantity": quantity,
                "size": size.name if size else "Small",
                "customization": customization if customization else "",
                "image": product.image.url if product.image else "",
            }
        request.session["cart"] = cart
        request.session.modified = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
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
    cart_items = []
    total_price = 0
    if request.user.is_authenticated:
        db_cart_items = CartItem.objects.filter(user=request.user)
        for item in db_cart_items:
            subtotal = item.adjusted_price * item.quantity
            total_price += subtotal
            cart_items.append({
                "product_id": item.product.id,
                "size_id": item.size.id if item.size else None,
                "name": item.product.name,
                "image": item.product.image.url if item.product.image else None,
                "price": item.adjusted_price,
                "quantity": item.quantity,
                "size": item.size.name if item.size else "N/A",
                "customization": item.customization or "",
                "subtotal": subtotal,
                "update_url": reverse("cart_update", args=[item.product.id, item.size.id if item.size else 0]),
                "remove_url": reverse("cart_remove", args=[item.product.id, item.size.id if item.size else 0]),
            })
    else:
        session_cart = request.session.get("cart", {})
        for key, item in session_cart.items():
            if "_" in key:
                product_id, size_id = key.split("_")
            else:
                product_id, size_id = key, None
            try:
                product = Product.objects.get(id=product_id)
                size = Size.objects.get(id=size_id) if size_id else None
            except (Product.DoesNotExist, Size.DoesNotExist):
                continue
            subtotal = float(item["price"]) * item["quantity"]
            total_price += subtotal
            cart_items.append({
                "product_id": product.id,
                "size_id": size.id if size else None,
                "name": product.name,
                "image": product.image.url if product.image else None,
                "price": float(item["price"]),
                "quantity": item["quantity"],
                "size": size.name if size else "N/A",
                "customization": item.get("customization", ""),
                "subtotal": subtotal,
                "update_url": reverse("cart_update", args=[product.id, size.id if size else 0]),
                "remove_url": reverse("cart_remove", args=[product.id, size.id if size else 0]),
            })

    return render(request, "orders/cart.html", {"cart": cart_items, "total_price": total_price})

def cart_remove(request, product_id, size_id=0):
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
    """Handles order checkout, validation, and Stripe payment initiation."""
    cart_items = []
    total_price = Decimal("0.00")

    if request.user.is_authenticated:
        db_cart_items = CartItem.objects.filter(user=request.user)
        if not db_cart_items.exists():
            messages.error(request, "Your cart is empty!")
            return redirect("cart_view")
        for item in db_cart_items:
            subtotal = item.adjusted_price * item.quantity
            total_price += subtotal
            cart_items.append({
                "product": item.product, 
                "size": item.size,
                "quantity": item.quantity, 
                "price": item.adjusted_price,
                "subtotal": subtotal
            })
    else:
        session_cart = request.session.get("cart", {})
        if not session_cart:
            messages.error(request, "Your cart is empty!")
            return redirect("cart_view")
        for key, item in session_cart.items():
            if "_" in key:
                product_id, size_id = key.split("_")
            else:
                product_id, size_id = key, None
            try:
                product = Product.objects.get(id=product_id)
                size = Size.objects.get(id=size_id) if size_id else None
            except (Product.DoesNotExist, Size.DoesNotExist):
                continue
            subtotal = Decimal(item["price"]) * item["quantity"]
            total_price += subtotal
            cart_items.append({
                "product": product,
                "size": size,
                "quantity": item["quantity"],
                "price": Decimal(item["price"]),
                "subtotal": subtotal
            })

    # Calculate delivery charge (adjust according to your settings)
    delivery_charge = Decimal("0.00") if total_price >= Decimal(settings.FREE_DELIVERY_THRESHOLD) else Decimal(settings.STANDARD_DELIVERY_CHARGE)
    grand_total = total_price + delivery_charge

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            # Create order items for each cart item
            for item in cart_items:
                OrderItem.objects.create(
                    order=order, 
                    product=item["product"],
                    size=item.get("size"),
                    quantity=item["quantity"],
                    price_each=item["price"]
                )

            messages.success(request, "Order placed! Redirecting to payment.")
            return redirect(reverse("create_checkout_session"))
        messages.error(request, "Please fix the errors in the form.")
    else:
        form = OrderForm(initial={"email": request.user.email} if request.user.is_authenticated else {})

    return render(request, "orders/checkout.html", {
        "form": form, 
        "cart_items": cart_items, 
        "total_price": total_price, 
        "delivery_charge": delivery_charge, 
        "grand_total": grand_total
    })

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/order_history.html", {"orders": orders})

@login_required
def custom_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = CustomOrderForm(request.POST)
        if form.is_valid():
            custom_message = form.cleaned_data["custom_message"]
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
    new_quantity = request.POST.get("quantity")
    if not new_quantity or not new_quantity.isdigit():
        messages.error(request, "Invalid quantity.")
        return HttpResponseRedirect(reverse("cart_view"))
    new_quantity = int(new_quantity)
    if request.user.is_authenticated:
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
        request.session.modified = True
    return HttpResponseRedirect(reverse("cart_view"))

@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    cart = request.session.get("cart", {})
    for key, item in cart.items():
        if "_" in key:
            product_id, size_id = key.split("_")
        else:
            product_id, size_id = key, None
        product = get_object_or_404(Product, id=product_id)
        size = get_object_or_404(Size, id=size_id) if size_id else None
        cart_item, created = CartItem.objects.get_or_create(
            user=user, product=product, size=size,
            defaults={"quantity": item["quantity"], "customization": item.get("customization", "")}
        )
        if not created:
            cart_item.quantity += item["quantity"]
        cart_item.save()
    request.session["cart"] = {}

@receiver(user_logged_out)
def clear_cart_on_logout(sender, request, user, **kwargs):
    request.session["cart"] = {}
    request.session.modified = True

@require_POST
def create_checkout_session(request):
    """
    Handles order creation and initiates a Stripe Checkout session.
    """
    form = OrderForm(request.POST)
    if not form.is_valid():
        return JsonResponse({
            "error": "Invalid billing details. Please check your input.",
            "form_errors": form.errors
        }, status=400)

    new_order = form.save(commit=False)
    if request.user.is_authenticated:
        new_order.user = request.user
    new_order.save()

    # Debug log: check that order_number exists
    print(f"✅ Order Created: {new_order.order_number}")

    cart_items = []
    if request.user.is_authenticated:
        cart_items = list(CartItem.objects.filter(user=request.user))
    else:
        session_cart = request.session.get("cart", {})
        if not session_cart:
            return JsonResponse({"error": "Your cart is empty. Cannot proceed to payment."}, status=400)
        for key, item in session_cart.items():
            if "_" in key:
                product_id, size_id = key.split("_")
            else:
                product_id, size_id = key, None
            try:
                product = Product.objects.get(id=product_id)
                size = Size.objects.get(id=size_id) if size_id else None
            except (Product.DoesNotExist, Size.DoesNotExist):
                continue
            cart_items.append({
                "product": product,
                "size": size,
                "quantity": item.get("quantity", 1),
                "price": Decimal(item.get("price", 0))
            })

    if not cart_items:
        return JsonResponse({"error": "Your cart is empty. Cannot proceed to payment."}, status=400)

    line_items = []
    for item in cart_items:
        try:
            if isinstance(item, CartItem):
                product = item.product
                quantity = item.quantity
                price = item.adjusted_price
                size = item.size
            else:
                product = item["product"]
                quantity = item["quantity"]
                price = item["price"]
                size = item.get("size")
            # Store OrderItem in database (including size if available)
            OrderItem.objects.create(
                order=new_order,
                product=product,
                size=size,
                quantity=quantity,
                price_each=price
            )
            line_items.append({
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': product.name},
                    'unit_amount': int(price * 100),
                },
                'quantity': quantity,
            })
        except Product.DoesNotExist:
            return JsonResponse({"error": f"Product {product.id} not found."}, status=400)

    metadata = {
        "order_number": str(new_order.order_number),
        "customer_email": new_order.email or "unknown@example.com"
    }
    print(f"✅ Stripe Metadata: {metadata}")

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri(reverse('payment_success')),
            cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
            metadata=metadata,
            payment_intent_data={"metadata": metadata},
        )
        print(f"✅ Stripe Checkout Session Created: {checkout_session.id}")
        print(f"✅ Stripe Checkout Session Metadata: {checkout_session.metadata}")
        return redirect(checkout_session.url)
    except stripe.error.StripeError as e:
        print(f"❌ Stripe Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)

def payment_success(request):
    return render(request, "orders/payment_success.html")

def payment_cancel(request):
    return render(request, "orders/payment_cancel.html")

@csrf_exempt
def stripe_webhook(request):
    """Listen for Stripe webhooks and pass them to the handler."""
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    from .webhook_handler import StripeWH_Handler
    handler = StripeWH_Handler(request)
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Map event types to handler methods
    event_map = {
        "checkout.session.completed": handler.handle_checkout_session_completed,
        "payment_intent.succeeded": handler.handle_payment_intent_succeeded,
        "payment_intent.payment_failed": handler.handle_payment_intent_payment_failed,
    }
    event_handler = event_map.get(event["type"], handler.handle_event)
    response = event_handler(event)
    return response