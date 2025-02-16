from django.contrib.auth import views
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.db.models import Q, Sum
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm
import stripe
import logging

from .models import LibraryCustomer, CurrentLoan, LoanHistory, Fine 

logger = logging.getLogger(__name__)

@login_required
def find_users(request):
    return render(request, 'users/users_home.html' )

@login_required
def search_users(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        # Split the query into separate words
        search_terms = query.split()
        filters = Q()  # Start with an empty Q object

        for term in search_terms:
            # Create Q objects for each term to match first or last names
            filters |= Q(first_name__icontains=term) | Q(last_name__icontains=term) | Q(user_id__icontains=term)

        results = list(LibraryCustomer.objects.filter(filters).values('first_name', 'last_name', 'email_address', 'user_id'))

    return JsonResponse(results, safe=False)

@login_required
def display_customer_details(request, user_id):
    """
    A view to display and edit customer details.
    """
    library_customer = get_object_or_404(LibraryCustomer, user_id=user_id)
    
    current_loans = CurrentLoan.objects.filter(
            customer=user_id
            ).order_by('due_date')

    fines = Fine.objects.filter(
            customer=library_customer
            ).order_by('date_issued')

    total_fines = fines.aggregate(total=Sum('amount'))['total']

    total_fines = total_fines or 0

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=library_customer)
        if form.is_valid():
            form.save()
            return redirect('home')
        else: 
            print(form.errors)
    else:
        form = CustomerForm(instance=library_customer)

    context = {
        'current_loans': current_loans,
        'customer': library_customer,
        'form': form,
        'user_id': user_id,
        'fines': fines,
        'total_fines': total_fines,
    }

    return render(request, 'users/customer_details.html', context)

@login_required
def add_library_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            new_customer = form.save()
            return redirect(reverse('display_customer_details', args=[new_customer.user_id]))
    else: 
        form = CustomerForm()
    
    template = 'users/add_new_user.html'
    context = {
        'form': form,
    }
    return render(request, template, context)

@login_required
def edit_library_customer(request, user_id):
    library_customer = get_object_or_404(LibraryCustomer, pk=user_id)
    user_id=user_id
    current_loans = CurrentLoan.objects.filter(
            customer=library_customer
            ).order_by('due_date')

    fines = Fine.objects.filter(
            customer=library_customer
            ).order_by('date_issued')

    total_fines = fines.aggregate(total=Sum('amount'))['total']

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=library_customer)
        if form.is_valid():
            form.save()
            return redirect(reverse('display_customer_details', args=[user_id]))
    else: 
        form = CustomerForm(instance=library_customer)

    template = 'users/customer_details.html'  # Updated template path
    context = {
        'form': form,
        'library_customer': library_customer,
        'user_id': user_id,
        'current_loans': current_loans,
        'fines': fines,
        'total_fines': total_fines,
    }

    return render(request, template, context)

@login_required
def customer_loan_history(request, user_id):
        customer = get_object_or_404(LibraryCustomer, user_id=user_id)
        
        loan_history_list = LoanHistory.objects.filter(customer=customer).order_by('-check_out_date')  # Changed from loan_date
        
        paginator = Paginator(loan_history_list, 10)
        page = request.GET.get('page')
        
        try:
            loan_history = paginator.page(page)
        except PageNotAnInteger:
            loan_history = paginator.page(1)
        except EmptyPage:
            loan_history = paginator.page(paginator.num_pages)
        
        context = {
            'customer': customer,
            'loan_history': loan_history,
            'user_id': user_id,
        }
        return render(request, 'users/loan_history.html', context)

@login_required
def delete_library_customer(request, user_id):
    library_customer = get_object_or_404(LibraryCustomer, pk=user_id)
    library_customer.delete()
    
    return redirect(reverse('find_users'))


@login_required
def payment_page(request, fine_id):
    fine = get_object_or_404(Fine, fine_id=fine_id)
    context = {
        'fine': fine,
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, 'users/payment.html', context)

@login_required
def create_payment_intent(request, fine_id):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        fine = get_object_or_404(Fine, fine_id=fine_id)
        print("creating intent")
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(fine.amount * 100),
                currency='gbp',
                metadata={'fine_id': str(fine_id),
                          'user_id': str(fine.customer.user_id),
                          }  # Ensure fine_id is a string
            )
            
            # Log the entire intent object for debugging
            client_secret = intent.client_secret
            client_secret_string = str(client_secret)
            return JsonResponse({
                'clientSecret': client_secret_string
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# views.py
def process_payment_success(fine_id):
    """
    Process a successful payment for a given fine_id.
    """
    print("process_payment_success started...")
    try:
        fine = get_object_or_404(Fine, fine_id=fine_id)
        return {
                'status': 'success',
                'fine': fine,
                'date_paid': fine.date_paid,
                'amount': fine.amount
            }
        
    except Exception as e:
        print(f"Error in process_payment_success: {str(e)}")
        return {
            'status': 'error',
            'message': 'An error occurred while processing your payment'
        }

@login_required
def payment_success(request, fine_id):
    # Initialize the Stripe webhook handler
    print("payment success started...")
    stripe_handler = StripeWH_Handler(request)

    # Process the payment success
    payment_successful = stripe_handler.process_payment_success(fine_id)

    if payment_successful:
        # Fetch the fine and customer details
        print("payment successful")
        fine = get_object_or_404(Fine, fine_id=fine_id)
        customer = get_object_or_404(LibraryCustomer, user_id=fine.customer.user_id)

        # Render the success template
        return render(request, 'users/payment_success.html', {
            'fine': fine,
        })
    else:
        # Render the error template if payment processing fails
        print("payment error")
        return render(request, 'users/payment_error.html', {
            'message': 'An error occurred while processing your payment.'
        })
@login_required
def customer_fine_history(request, user_id):
        customer = get_object_or_404(LibraryCustomer, user_id=user_id)

        fine_history_list = Fine.objects.filter(customer=customer).order_by('date_issued')  # Changed from loan_date
        
        paginator = Paginator(fine_history_list, 10)
        page = request.GET.get('page')
        
        try:
            fine_history = paginator.page(page)
        except PageNotAnInteger:
            fine_history = paginator.page(1)
        except EmptyPage:
            fine_history = paginator.page(paginator.num_pages)
        
        context = {
            'customer': customer,
            'fine_history': fine_history,
            'user_id': user_id,
        }
        return render(request, 'users/fine_history.html', context)

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request
        self.logger = logging.getLogger('stripe_webhook')

    def handle_event(self, event):
        """
        Handle a generic/unknown webhook event
        """
        self.logger.info(f"Unhandled webhook event: {event['type']}")
        return HttpResponse(status=200)

    def handle_payment_intent_succeeded(self, event):
        print("handle_Payment_intent_succeeded started...")
        payment_intent = event['data']['object']
        fine_id = payment_intent.get('metadata', {}).get('fine_id')
        
        if not fine_id:
            print("No fine_id found in payment_intent metadata")
            return HttpResponse(status=400)
        
        # Process the payment success
        if self.process_payment_success(fine_id):
            print("process_payment_success success...")
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)

    def process_payment_success(self, fine_id):
        """
        Reusable method to process payment success for a given fine_id.
        """
        print("process_payment_success started...")
        try:
            fine = Fine.objects.get(fine_id=fine_id)
            customer = fine.customer
            print("process_payment_success fine:", fine.fine_id)
            customer.pay_fine(fine.fine_id)  # Call the pay_fine method
            print(f"Payment processed successfully for fine_id: {fine_id}")
            return True
        
        except Exception as e:
            print(f"Error processing payment for fine_id: {fine_id} - {str(e)}")
            return False    

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook event
        """
        print("Payment intent failed")
        
        return HttpResponse(status=200)
