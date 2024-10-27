from django.contrib import admin
from .models import CatalogueItem, StockItem 

admin.site.register(CatalogueItem)
admin.site.register(StockItem)

# Register your models here.
