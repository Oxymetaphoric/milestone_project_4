from django.db import models

# Create your models here.

class LibraryCustomer(models.Model):
    user_id = models.CharField(primary_key=True, max_length=8, unique=True, blank=True, editable=False)
    first_name = models.CharField(max_length=256, blank=True, null=True) 
    last_name = models.CharField(max_length=256, blank=False, null=False)
    street_address1 = models.CharField(max_length=256, blank=False, null=False)
    street_address2 = models.CharField(max_length=256, blank=True, null=True)
    city_or_town = models.CharField(max_length=256, blank=False, null=False)
    postcode = models.CharField(max_length=20, blank=False, null=False)
    phone_number = models.CharField(max_length=25, blank=False, null=False)
    email_address = models.CharField(max_length=256, blank=False, null=False)
    is_child = models.BooleanField()
    date_of_birth = models.DateField()
    
    def save(self, *args, **kwargs):
        if not self.user_id:  # Only set username if it's not already set
            user_count = LibraryCustomer.objects.count()
            next_number = user_count + 1  # Start from 1

            prefix = 'A'
            max_count_per_prefix = 9999999

            # Check if we need to increment the prefix
            if next_number > max_count_per_prefix:
                next_number = 1  # Reset to 1 for the new prefix
                prefix = chr(ord(prefix) + (user_count // max_count_per_prefix))  # Increment the letter

            self.user_id = f"{prefix}{next_number:07d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user_id)


