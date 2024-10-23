from django.db import models

# Create your models here.

""""
the dictionary provided w/ the dataset can be queried directly

class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=354, null=True, blank=True)
"""

"""
this model needs moving to the User app when created

class User(models.Model):
    first_name = models.CharField(max_length=256, blank=False, null=False) 
    last_name = models.CharField(max_length=256, blan ek=False, null=False)
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
"""

class StockItem(models.Model):
    BibNum = models.CharField(max_length=256, null=False, blank=False)
    Title = models.CharField(max_length=512, null=False, blank=False)
    Author = models.CharField(max_length=512, null=False, blank=False)
    ISBN = models.CharField(max_length=256, null=True, blank=True) 
    PublicationYear = models.IntegerField()
    Publisher = models.CharField(max_length=256, null=False, blank=False)
    Subjects = models.TextField()
    ItemType = models.CharField(max_length=128, null=False, blank=False)
    ItemCollection = models.CharField(max_length=128, null=False, blank=False)
    FloatingItem = models.CharField(max_length=256, null=True, blank=True)
    ItemLocation = models.CharField(max_length=128, null=False, blank=False)
    ReportDate = models.DateField()
    ItemCount = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.title

