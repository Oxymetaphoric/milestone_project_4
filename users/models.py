from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length=128, blank=True, null=True)
    first_name = models.CharField(max_length=256, blank=True, null=True) 
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
        return self.first_name + self.last_name


