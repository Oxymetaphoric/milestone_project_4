import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from users.models import Fine, Payment 

STRIPE_API_KEY=settings.STRIPE_API_KEY

@require_POST
@csrf_exempt
def stripe_webhook(request):
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    print("Webhook received")
    print("Request method:", request.method)
    print("Stripe-Signature header:", request.headers.get('Stripe-Signature'))
    print("secret:", webhook_secret)

    try:
        payload = request.body.decode # Ensure proper string format
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        print("Raw request body:", request.body)
        event = stripe.Webhook.construct_event(
            payload,  sig_header, webhook_secret
        )
        print("construct event complete")
        
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            print("PaymentIntent succeeded:", payment_intent['id'])
            
            # fine_id = payment_intent['metadata'].get('fine_id')
            # print("fine_id from metadata:", fine_id)
            # 
            # if fine_id:
            #     try:
            #         fine = Fine.objects.get(fine_id=fine_id)
            #         print("Fine found:", fine)
            #         
            #         customer = fine.customer
            #         print("Customer found:", customer)
            #         
            #         # Create payment record
            #         Payment.objects.create(
            #             fine=fine,
            #             stripe_payment_id=payment_intent['id'],
            #             status='COMPLETED'
            #         )
            #         print("Payment record created for fine:", fine_id)
            #         
            #         # Update fine status
            #         if customer.pay_fine(fine_id):
            #             print("Fine marked as paid:", fine_id)
            #         else:
            #             print("Failed to mark fine as paid:", fine_id)
            #     except Fine.DoesNotExist:
            #         print("Fine not found:", fine_id)
            # else:
            #     print("No fine_id in metadata")
    except Exception as e:
         print("Error processing fine:", str(e))
        
    return JsonResponse({'status': 'success'})

