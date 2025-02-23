import json
from django.http import HttpResponse
from .models import Order, CartItem  # ✅ Ensure both models are imported

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Handle unexpected webhook event"""
        print(f"⚠️ Unhandled webhook received: {event['type']}")  # Debugging
        return HttpResponse(
            content=f'⚠️ Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle successful payments and clear the cart"""
        intent = event["data"]["object"]  # Get the payment intent data

        print("🟢 Payment Success Event Received!")
        print(json.dumps(intent, indent=4))  # Pretty-print Stripe data for debugging

        # ✅ Ensure metadata exists before accessing order_number
        order_number = intent.get("metadata", {}).get("order_number")

        if not order_number:
            print("❌ No order_number found in metadata! Ensure it's set in create_checkout_session.")
            return HttpResponse(
                content="❌ No order_number in webhook metadata.",
                status=400
            )

        try:
            order = Order.objects.get(order_number=order_number)
            order.status = "paid"
            order.save()
            print(f"✅ Order {order_number} marked as PAID.")

            # ✅ Clear cart after successful payment
            if order.user:
                CartItem.objects.filter(user=order.user).delete()
            else:
                if "cart" in self.request.session:
                    del self.request.session["cart"]
                    self.request.session.modified = True

            return HttpResponse(
                content=f'✅ Webhook received: {event["type"]} - Order {order_number} marked as paid.',
                status=200
            )

        except Order.DoesNotExist:
            print(f"❌ Order {order_number} NOT found in database.")
            return HttpResponse(
                content=f'❌ Webhook received: {event["type"]} - Order not found!',
                status=400
            )

    def handle_payment_intent_payment_failed(self, event):
        """Handle failed payments"""
        intent = event["data"]["object"]

        print("🔴 Payment Failed Event Received!")
        print(json.dumps(intent, indent=4))  # Debugging failed payment

        order_number = intent.get("metadata", {}).get("order_number")

        if not order_number:
            print("❌ No order_number found in metadata for failed payment.")
            return HttpResponse(
                content="❌ No order_number in webhook metadata for failed payment.",
                status=400
            )

        try:
            order = Order.objects.get(order_number=order_number)
            order.status = "pending"  # ✅ Keep order as pending
            order.save()
            print(f"⚠️ Order {order_number} remains PENDING due to failed payment.")

            return HttpResponse(
                content=f'⚠️ Webhook received: {event["type"]} - Payment failed for Order {order_number}.',
                status=200
            )

        except Order.DoesNotExist:
            print(f"❌ Order {order_number} not found for failed payment.")
            return HttpResponse(
                content=f'⚠️ Webhook received: {event["type"]} - Order not found for failed payment.',
                status=400
            )