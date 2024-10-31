from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.db.models import Q
from django.http import JsonResponse
from .models import CatalogueItem, StockItem 
from .forms import StockForm

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
            # Create Q objects for each term to match first or last names
            filters |= Q(Title__icontains=term) | Q(Author__icontains=term) | Q(Publisher__icontains=term)
            results = list(
                CatalogueItem.objects.filter(filters)
                .prefetch_related('stock_items')  # Use prefetch_related if there's a reverse relationship
                .values('Title', 'Author', 'Publisher', 'stock_items__StockID')
                )
    print("search results:", results)
    return JsonResponse(results, safe=False)


def edit_stock_item(request, StockID):
    """
    A view to display and edit customer details.
    """
    stock_item = get_object_or_404(StockItem, StockID=StockID)
    catalogue = CatalogueItem.objects.prefetch_related('stock_items').all()
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock_item)
        if form.is_valid():
            stock_item = form.save(commit=False)
            new_item_count = form.cleaned_data['item_count']
            stock_item.catalogue_item.ItemCount = new_item_count  # Update CatalogueItem's ItemCount
            stock_item.save()
            stock_item.catalogue_item.save()
            return redirect('catalogue')
    else:
        form = StockForm(instance=stock_item)

    template = 'catalogue/item_details.html'  # Updated template path
    context = {
        'stock_item': stock_item,
        'form': form,
        'catalogue': catalogue,
    }

    return render(request, template, context)


def remove_stock_item(request, StockID):
    stock_item = get_object_or_404(StockItem, StockID=StockID)
    stock_item.delete()
    return redirect(reverse('catalogue'))

