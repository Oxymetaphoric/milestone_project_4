import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from users.models import LibraryCustomer, Fine, Payment 
from django.utils import timezone

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    
    try:
        event = stripe.Webhook.construct_event(
            payload=request.body,
            sig_header=request.headers.get('Stripe-Signature'),
            secret=webhook_secret
        )
        
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            fine_id = payment_intent['metadata']['fine_id']
            fine = Fine.objects.get(fine_id=fine_id)
            
            # Create payment record
            Payment.objects.create(
                fine=fine,
                stripe_payment_id=payment_intent['id'],
                status='COMPLETED'
            )
            
            # Update fine status
            fine.is_paid = True
            fine.date_paid = timezone.now()
            fine.save()
            
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
