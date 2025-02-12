from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from users.models import LibraryCustomer, CurrentLoan, LoanHistory, Fine, Payment 
from .forms import CustomerForm
import stripe

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

def create_payment_intent(request, fine_id):
    if request.method=='POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        fine = get_object_or_404(Fine, fine_id=fine_id)
        
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(fine.amount * 100),
                currency='gbp',
                metadata={'fine_id': str(fine.fine_id)}
            )
            return JsonResponse({
                'clientSecret': intent.client_secret
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

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

