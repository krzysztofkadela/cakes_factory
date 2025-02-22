from django.http import HttpResponse
from .models import Order

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Handle generic/unexpected webhook event"""
        return HttpResponse(
            content=f'Unhandled event received: {event["type"]}',
            status=200
        )

    def handle_checkout_session_completed(self, event):
        """
        Handle the checkout.session.completed event
        Update the order status when payment is successful.
        """
        session = event["data"]["object"]
        order_number = session.get("metadata", {}).get("order_number")

        if order_number:
            try:
                order = Order.objects.get(order_number=order_number)
                order.status = "paid"
                order.save()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Order marked as paid',
                    status=200
                )
            except Order.DoesNotExist:
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: Order not found',
                    status=404
                )

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | WARNING: Order number missing',
            status=400
        )