from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import uuid

# Create your models here.

""""
the dictionary provided w/ the dataset can be queried directly

class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=354, null=True, blank=True)
"""

class CatalogueItem(models.Model):
    BibNum = models.CharField(primary_key=True, max_length=256, null=False, blank=False)
    Title = models.CharField(max_length=512, null=False, blank=False)
    Author = models.CharField(max_length=512, null=False, blank=False)
    ISBN = models.CharField(max_length=256, null=True, blank=True) 
    PublicationYear = models.CharField(max_length=256, null=True, blank=True)
    Publisher = models.CharField(max_length=256, null=False, blank=False)
    Subjects = models.CharField(max_length=256, null=False, blank=False)
    ItemType = models.CharField(max_length=128, null=False, blank=False)
    ItemCollection = models.CharField(max_length=128, null=False, blank=False)
    FloatingItem = models.CharField(max_length=256, null=True, blank=True)
    ItemLocation = models.CharField(max_length=128, null=False, blank=False)
    ReportDate = models.CharField(max_length=256, null=False, blank=False)
    ItemCount = models.IntegerField(default=0, null=True, blank=True)
    
    def update_item_count(self):
        self.ItemCount = self.stock_items.count()
        self.save()

    def __str__(self):
        return self.Title


class StockItem(models.Model):
    StockID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    catalogue_item = models.ForeignKey(CatalogueItem, on_delete=models.CASCADE, related_name='stock_items')
    
    def __str__(self):
        return str(self.StockID)

@receiver(post_save, sender=StockItem)
@receiver(post_delete, sender=StockItem)
def update_catalogue_item_count(sender, instance, **kwargs):
    instance.catalogue_item.update_item_count()

