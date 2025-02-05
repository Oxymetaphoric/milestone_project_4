from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import CatalogueItem, StockItem 
from users.models import LibraryCustomer, CurrentLoan, LoanHistory 
from .forms import StockForm
import uuid

# Create your views here.

def display_catalogue_items(request):

    """
    A view to display, search, and sort catalogue items
    """
    catalogue = CatalogueItem.objects.prefetch_related('stock_items').all()
    context = {
            'catalogue': catalogue,
            }
    return render(request, 'catalogue/catalogue.html', context)

def display_stock_items(request):
    stock_item=StockItem.objects.all()
    context = {
            'stock_items': stock_item,
            }
    return render(request, 'catalogue/item_details.html', context)

def search_catalogue(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        # Split the query into separate words
        search_terms = query.split()
        filters = Q()  # Start with an empty Q object
        for term in search_terms:
            # Create Q objects for each term to match fields
            filters |= (
                Q(Title__icontains=term) | 
                Q(Author__icontains=term) | 
                Q(Publisher__icontains=term) 
            )
        
        # Get CatalogueItems and include BibNum as the identifier
        results = list(
            CatalogueItem.objects.filter(filters)
            .prefetch_related('stock_items')
            .values(
                'BibNum',  # Use BibNum instead of id
                'Title', 
                'Author', 
                'Publisher',
                'ItemCount'
            )
        )
    
    return JsonResponse(results, safe=False)

def book_info(request, BibNum): 
    catalogue_item = get_object_or_404(CatalogueItem, pk=BibNum)
    stock_items = catalogue_item.stock_items.all()
    
    if request.method == 'POST':        
        if 'add_copies' in request.POST:
            try:
                quantity = int(request.POST.get('quantity', 1))
                for _ in range(quantity):
                    StockItem.objects.create(
                        catalogue_item=catalogue_item,
                    )
                catalogue_item.ItemCount = StockItem.objects.filter(catalogue_item=catalogue_item).count()
                catalogue_item.save()
                messages.success(request, f'Added {quantity} new copies successfully.')
            except ValueError:
                messages.error(request, 'Invalid quantity specified.')
            
        elif 'delete_stock_item' in request.POST:
            stock_id = request.POST.get('stock_id')
            try:
                stock_item = StockItem.objects.get(pk=stock_id)
                stock_item.delete()
                catalogue_item.ItemCount = StockItem.objects.filter(catalogue_item=catalogue_item).count()
                catalogue_item.save()
                messages.success(request, 'Stock item deleted successfully.')
            except StockItem.DoesNotExist:
                messages.error(request, 'Stock item not found.')
                
        elif 'update_stock_item' in request.POST:
            stock_id = request.POST.get('stock_id')
            new_status = request.POST.get('status')
            try:
                stock_item = StockItem.objects.get(pk=stock_id)
                stock_item.Status = new_status
                stock_item.save()
                messages.success(request, 'Stock item updated successfully.')
            except StockItem.DoesNotExist:
                messages.error(request, 'Stock item not found.')
                
        return redirect('book_info', BibNum=BibNum)

    context = {
        'catalogue_item': catalogue_item,
        'stock_items': stock_items,
        'BibNum': BibNum,
        }
    return render(request, 'catalogue/item_details.html', context)

def check_out(request):
    if request.method == 'POST':
        stock_id = request.POST.get('stock_id')
        user_id = request.POST.get('user_id')
        if stock_id and user_id:
            try:
                stock_id = uuid.UUID(stock_id)
                stock_item = StockItem.objects.get(StockID=stock_id)
                user = LibraryCustomer.objects.get(user_id=user_id)
                
                # Update stock item
                stock_item.Status = 'on_loan'
                stock_item.Location = user.user_id
                stock_item.Borrower = user.user_id
                stock_item.save()
                
                messages.success(
                    request,
                    f'Successfully checked out: {stock_item.Title} to user: {user.user_id}'
                )
            except ValueError:
                messages.error(request, 'Invalid ID format')
            except ObjectDoesNotExist:
                messages.error(request, 'Item or user not found')
        else:
            messages.error(request, 'Please enter both Stock ID and User ID')
    return render(request, 'catalogue/check_out.html')

def check_in(request):
    if request.method == 'POST':
        stock_id = request.POST.get('stock_id')
        if stock_id:
            try:
                stock_id = uuid.UUID(stock_id)
                stock_item = StockItem.objects.get(StockID=stock_id)
                
                # Update stock item
                stock_item.Status = 'available'
                stock_item.Location = 'In Branch'
                stock_item.Borrower = None
                stock_item.save()
                
                messages.success(
                    request,
                    f'Successfully checked in: {stock_item.Title} (ID: {stock_item.StockID})'
                )
            except ValueError:
                messages.error(request, 'Invalid Stock ID format')
            except StockItem.DoesNotExist:
                messages.error(request, 'Stock item not found')
        else:
            messages.error(request, 'Please enter a Stock ID')
    return render(request, 'catalogue/check_in.html')
