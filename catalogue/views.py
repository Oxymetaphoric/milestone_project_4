from django.shortcuts import render
from .models import CatalogueItem 

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
