# import logging
# from django.dispatch import receiver
# from djstripe.signals import webhook_post_validate

# logger = logging.getLogger(__name__)

# @receiver(webhook_post_validate)
# def handle_webhook_event(sender, instance, **kwargs):
#     print("webhook intitialised")
#     if instance.event_type == "payment_intent.succeeded":
#         payment_intent = instance.data["object"]
#         print(f"PaymentIntent succeeded: {payment_intent['id']}")

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .views import StripeWH_Handler  # Ensure this import is correct
import stripe
import logging

# Set up logging
logger = logging.getLogger(__name__)

@require_POST
@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe"""
    print("Webhook initialized")

    # Setup
    wh_secret = settings.DJSTRIPE_WEBHOOK_SECRET

    # Get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:
        # Invalid payload
        logger.error(f"Invalid payload: {e}")
        return HttpResponse(status=400)
    except Exception as e:
        # Unexpected error
        logger.error(f"Unexpected error: {e}")
        return HttpResponse(status=500)

    # Set up a webhook handler
    handler = StripeWH_Handler(request)
    # Map webhook events to relevant handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    # Get the webhook type from Stripe
    event_type = event['type']

    # If there is a handler for it, get it from the event map
    # Use the generic one by default
    event_handler = event_map.get(event_type, handler.handle_event)

    # Call the event handler with the event
    response = event_handler(event)
    return response
