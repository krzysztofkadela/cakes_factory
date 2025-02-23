from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .webhook_handler import StripeWH_Handler  # Ensure correct import path
import stripe

@require_POST
@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe and process them securely."""

    # Setup Stripe API keys
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Retrieve and verify webhook payload
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")  # Use `.get()` to avoid KeyError
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, wh_secret)
    except ValueError:
        return HttpResponse("Invalid payload", status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse("Invalid signature", status=400)
    except Exception as e:
        return HttpResponse(f"Error processing webhook: {str(e)}", status=400)

    # Instantiate the webhook handler
    handler = StripeWH_Handler(request)

    # Map webhook events to handler methods
    event_map = {
        "payment_intent.succeeded": handler.handle_payment_intent_succeeded,
        "payment_intent.payment_failed": handler.handle_payment_intent_payment_failed,
    }

    # Determine the event type
    event_type = event.get("type", "unknown_event")

    # Get the corresponding handler, or use the default handler
    event_handler = event_map.get(event_type, handler.handle_event)

    # Execute the event handler and return its response
    return event_handler(event)