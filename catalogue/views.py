from django.shortcuts import render
from .models import StockItem 

# Create your views here.

def display_stock_items(request):
    """
    A view to display, search, and sort catalogue items
    """
    catalogue = StockItem.objects.all()

    context = {
            'catalogue': catalogue,
            }

    return render(request, 'catalogue/catalogue.html', context)
