from django.db import models

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
    ItemCount = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.Title

"""
class StockItem(models.Model):
    StockID = models.CharField(primary_key=True,  max_length=256)
    catalogue_item = models.ForeignKey(CatalogueItem, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.Title
"""
