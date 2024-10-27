from django.core.management.base import BaseCommand
from catalogue.models import CatalogueItem, StockItem

class Command(BaseCommand):
    help = "Create StockItem instances based on CatalogueItem's ItemCount field"

    def handle(self, *args, **kwargs):
        # Loop through each CatalogueItem and create the initial StockItems
        for item in CatalogueItem.objects.all():
            count = int(item.ItemCount or 0)
            for _ in range(count):
                StockItem.objects.create(catalogue_item=item)
        self.stdout.write(self.style.SUCCESS("StockItems created for each CatalogueItem's ItemCount"))
