from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=354, null=True, blank=True)
    
class User(models.Model):
    first_name = models.CharField(max_length=256, blank=False, null=False) 
    last_name = models.CharField(max_length=256, blank=False, null=False)
    street_address1 = models.CharField(max_length=256, blank=False, null=False)
    street_address2 = models.CharField(max_length=256, blank=True, null=True)
    city_or_town = models.CharField(max_length=256, blank=False, null=False)
    postcode = models.CharField(max_length=20, blank=False, null=False)
    phone_number = models.IntegerField(blank=False, null=False)
    email_address = models.CharField(max_length=256, blank=False, null=False)
    is_child = models.BooleanField()
    date_of_birth = models.DateField()

    def __str__(self):
        return self.last_name
    
class StockItem(models.Model):
    bib_num = models.DecimalField(max_digits=10, decimal_places=8, null=False, blank=False)
    title = models.CharField(max_length=354, null=False, blank=False)
    author = models.CharField(max_length=128, null=False, blank=False)
    isbn = models.CharField(max_length=15, null=True, blank=True) 
    publication_year = models.DateField()
    publisher = models.CharField(max_length=256, null=False, blank=False)
    subjects = models.TextField()
    item_type = models.CharField(max_length=128, null=False, blank=False)
    item_Collection = models.CharField(max_length=128, null=False, blank=False)
    floating_item = models.BooleanField()
    item_location = models.CharField(max_length=128, null=False, blank=False)
    report_date = models.DateField()
    item_count = models.IntegerField()

    def __str__(self):
        return self.title

