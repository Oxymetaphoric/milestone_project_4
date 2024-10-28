
from django.shortcuts import render, get_object_or_404, reverse, redirect 
from .models import LibraryCustomer 
from .forms import CustomerForm

def find_users(request):
    query= request.GET.get('search', '')
    users = LibraryCustomer.objects.filter(user_id__icontains=query) if query else LibraryCustomer.objects.all()

    context = {
            'users': users,
            'search-query': query,
            }
    return render(request, 'users/users_home.html', context)

def display_customer_details(request, user_id):
    """
    A view to display and edit customer details.
    """
    library_customer = get_object_or_404(LibraryCustomer, user_id=user_id)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=library_customer)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomerForm(instance=library_customer)

    context = {
        'customer': library_customer,
        'form': form,
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
    
    template = 'users/add_new_user.html'
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

    template = 'users/customer_details.html'  # Updated template path
    context = {
        'form': form,
        'library_customer': library_customer,
    }

    return render(request, template, context)

def delete_library_customer(request, user_id):
    library_customer = get_object_or_404(LibraryCustomer, pk=user_id)
    library_customer.delete()
    return redirect(reverse('home'))

