from django.http import HttpResponse
from .models import Order

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Handle unexpected webhook event"""
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle successful payments and clear the cart"""
        intent = event.data.object  # Get the payment intent data
        order_number = intent.metadata.get("order_number")

        try:
            order = Order.objects.get(order_number=order_number)
            order.status = "paid"
            order.save()

            # ✅ Clear cart now (only after successful payment)
            if order.user:
                CartItem.objects.filter(user=order.user).delete()
            else:
                self.request.session["cart"] = {}
                self.request.session.modified = True

            return HttpResponse(
                content=f'Webhook received: {event["type"]} - Order {order_number} marked as paid.',
                status=200
            )

        except Order.DoesNotExist:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} - Order not found.',
                status=400
            )