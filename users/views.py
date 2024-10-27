from django.shortcuts import render, get_object_or_404
from .models import LibraryCustomer 

# Create your views here.

def display_customer_details(request, user_id):
    """
    A view to display, add, and edit customer details
    """
    customer = get_object_or_404(LibraryCustomer, user_id=user_id)

    context = {
            'customer': customer,
            }

    return render(request, 'users/customer_details.html', context)


