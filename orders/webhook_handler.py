import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Order, CartItem

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Default handler for unhandled events."""
        print(f"⚠️ Unhandled webhook received: {event['type']}")
        return HttpResponse(
            content=f"Unhandled event type: {event['type']}", status=200)

    def handle_checkout_session_completed(self, event):
        """
        Handle the checkout.session.completed event from Stripe.
        Marks the order as paid, clears the cart,
        and updates user shipping info (if any).
        """
        session = event["data"]["object"]
        order_number = session.get("metadata", {}).get("order_number")

        if not order_number:
            print("❌ No order_number found in session metadata!")
            return HttpResponse(
                "No order_number in webhook metadata.", status=400)

        # Retrieve the matching order
        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            print(f"❌ Order {order_number} not found.")
            return HttpResponse("Order not found.", status=400)

        # Mark order as paid
        order.status = "paid"
        order.save()
        print(
            f"✅ Order {order_number} marked as PAID")

        # Clear cart (DB-based if user is authenticated; session cart if guest)
        if order.user:
            CartItem.objects.filter(user=order.user).delete()
        else:
            if "cart" in self.request.session:
                del self.request.session["cart"]
                self.request.session.modified = True

        """
          Update user shipping address if user is 
          authenticated AND shipping info is present.

        """
        shipping_info = session.get("shipping") 
        if order.user and shipping_info:
            address = shipping_info.get("address", {})
            order.user.shipping_full_name = shipping_info.get("name", "")
            order.user.shipping_street_address1 = address.get("line1", "")
            order.user.shipping_street_address2 = address.get("line2", "")
            order.user.shipping_city = address.get("city", "")
            order.user.shipping_postcode = address.get("postal_code", "")
            order.user.shipping_country = address.get("country", "")
            order.user.save()
            print("✅ User shipping address updated from Stripe Checkout Session.")

        return HttpResponse(f"Order {order_number} marked as paid.", status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle payment_intent.succeeded webhook events.
        Not always necessary if your logic is in checkout.session.completed,
        but can be used as a fallback or for custom flows.
        """
        intent = event["data"]["object"]
        print("🟢 Payment Success Event Received!")
        print(json.dumps(intent, indent=4))

        order_number = intent.get("metadata", {}).get("order_number")
        if not order_number:
            print("❌ No order_number found in metadata for payment_intent.succeeded.")
            return HttpResponse("No order_number in webhook metadata.", status=400)

        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            print(f"❌ Order {order_number} not found for payment_intent.succeeded.")
            return HttpResponse("Order not found.", status=400)

        # Mark order as paid
        order.status = "paid"
        order.save()
        print(f"✅ Order {order_number} marked as PAID (payment_intent_succeeded).")

        # Clear cart
        if order.user:
            CartItem.objects.filter(user=order.user).delete()
        else:
            if "cart" in self.request.session:
                del self.request.session["cart"]
                self.request.session.modified = True

        return HttpResponse(f"Order {order_number} marked as paid.", status=200)

    def handle_payment_intent_payment_failed(self, event):
        """Handle failed payment_intent events."""
        intent = event["data"]["object"]
        print("🔴 Payment Failed Event Received!")
        print(json.dumps(intent, indent=4))

        order_number = intent.get("metadata", {}).get("order_number")
        if not order_number:
            print("❌ No order_number found in metadata for failed payment.")
            return HttpResponse("No order_number in webhook metadata for failed payment.", status=400)

        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            print(f"❌ Order {order_number} not found for failed payment.")
            return HttpResponse("Order not found.", status=400)

        # Mark order status as pending (or whatever you prefer)
        order.status = "pending"
        order.save()
        print(f"⚠️ Order {order_number} remains pending due to failed payment.")

        return HttpResponse(f"Payment failed for Order {order_number}.", status=200)