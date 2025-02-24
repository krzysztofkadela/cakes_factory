import json
from django.http import HttpResponse
from .models import Order, CartItem
from django.shortcuts import get_object_or_404

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Default handler for unhandled events."""
        print(f"⚠️ Unhandled webhook received: {event['type']}")
        return HttpResponse(content=f"Unhandled event type: {event['type']}", status=200)

    def handle_checkout_session_completed(self, event):
        """Handle successful checkout sessions."""
        session = event["data"]["object"]
        order_number = session.get("metadata", {}).get("order_number")
        if not order_number:
            print("❌ No order_number found in metadata!")
            return HttpResponse("No order_number in webhook metadata.", status=400)
        try:
            order = Order.objects.get(order_number=order_number)
            order.status = "paid"
            order.save()
            print(f"✅ Order {order_number} marked as PAID via checkout.session.completed.")
            if order.user:
                CartItem.objects.filter(user=order.user).delete()
            else:
                if "cart" in self.request.session:
                    del self.request.session["cart"]
                    self.request.session.modified = True
            return HttpResponse(f"Order {order_number} marked as paid.", status=200)
        except Order.DoesNotExist:
            print(f"❌ Order {order_number} not found.")
            return HttpResponse("Order not found.", status=400)

    def handle_payment_intent_succeeded(self, event):
        """Handle payment_intent.succeeded webhook events."""
        intent = event["data"]["object"]
        print("🟢 Payment Success Event Received!")
        print(json.dumps(intent, indent=4))
        order_number = intent.get("metadata", {}).get("order_number")
        if not order_number:
            print("❌ No order_number found in metadata for payment_intent.succeeded.")
            return HttpResponse("No order_number in webhook metadata.", status=400)
        try:
            order = Order.objects.get(order_number=order_number)
            order.status = "paid"
            order.save()
            print(f"✅ Order {order_number} marked as PAID.")
            if order.user:
                CartItem.objects.filter(user=order.user).delete()
            else:
                if "cart" in self.request.session:
                    del self.request.session["cart"]
                    self.request.session.modified = True
            return HttpResponse(f"Order {order_number} marked as paid.", status=200)
        except Order.DoesNotExist:
            print(f"❌ Order {order_number} not found for payment_intent.succeeded.")
            return HttpResponse("Order not found.", status=400)

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
            order.status = "pending"
            order.save()
            print(f"⚠️ Order {order_number} remains pending due to failed payment.")
            return HttpResponse(f"Payment failed for Order {order_number}.", status=200)
        except Order.DoesNotExist:
            print(f"❌ Order {order_number} not found for failed payment.")
            return HttpResponse("Order not found.", status=400)