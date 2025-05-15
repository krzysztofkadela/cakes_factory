from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import stripe
from .webhook_handler import StripeWH_Handler


@require_POST
@csrf_exempt
def webhook(request):
    """
    Listen for webhooks from Stripe and process them securely.
    Includes shipping if 'shipping_address_collection'
    was added to Checkout Session.
    """
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    webhook_secret = settings.STRIPE_WH_SECRET

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        return HttpResponse("Invalid payload", status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse("Invalid signature", status=400)
    except Exception as e:
        return HttpResponse(f"Error processing webhook: {str(e)}", status=400)

    handler = StripeWH_Handler(request)
    event_map = {
        "checkout.session.completed": handler.handle_checkout_session_completed,
        "payment_intent.succeeded": handler.handle_payment_intent_succeeded,
        "payment_intent.payment_failed": handler.handle_payment_intent_payment_failed,
    }
    event_handler = event_map.get(event.get("type"), handler.handle_event)

    response = event_handler(event)
    return response
