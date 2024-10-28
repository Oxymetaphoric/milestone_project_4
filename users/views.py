
from django.shortcuts import render, get_object_or_404, reverse, redirect 
from .models import LibraryCustomer 
from .forms import CustomerForm

def display_customer_details(request, user_id):
    """
    A view to display, add, and edit customer details.
    """
    customer = get_object_or_404(LibraryCustomer, user_id=user_id)

    context = {
        'customer': customer,
    }

    return render(request, 'users/customer_details.html', context)

def add_library_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
    else: 
        form = CustomerForm()
    
    template = 'users/add_user.html'
    context = {
        'form': form,
    }
    return render(request, template, context)

def edit_library_customer(request, user_id):
    library_customer = get_object_or_404(LibraryCustomer, pk=user_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=library_customer)
        if form.is_valid():
            form.save()
            return redirect(reverse('display_customer_details', args=[user_id]))
    else: 
        form = CustomerForm(instance=library_customer)

    template = 'users/edit_user.html'  # Updated template path
    context = {
        'form': form,
        'library_customer': library_customer,
    }

    return render(request, template, context)

def delete_library_customer(request, user_id):
    library_customer = get_object_or_404(LibraryCustomer, pk=user_id)
    library_customer.delete()
    return redirect(reverse('home'))

