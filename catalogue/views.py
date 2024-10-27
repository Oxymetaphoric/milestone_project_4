from django.shortcuts import render
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
