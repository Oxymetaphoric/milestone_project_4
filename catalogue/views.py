from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from .models import CatalogueItem, StockItem 

# Create your views here.

def display_catalogue_items(request):
    """
    A view to display, search, and sort catalogue items
    """
    catalogue = CatalogueItem.objects.all()

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

        results = list(CatalogueItem.objects.filter(filters).values('Title', 'Author', 'Publisher'))
    print("search results:", results)
    return JsonResponse(results, safe=False)

