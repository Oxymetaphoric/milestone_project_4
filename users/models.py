from django.db import models
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal
import uuid

FINE_CAP = Decimal('10.00')
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
    
    def get_total_unpaid_fines(self):
        return self.fines.filter(is_paid=False).aggregate(
                total=models.Sum('amount')['total'] or Decimal('0.00'))

    def pay_fine(self, fine_id):
        print("paying fine...")
        try:
            fine = self.fines.get(fine_id=fine_id, is_paid=False)
            print("fine is:", fine)
            fine.is_paid = True
            print("is paid: ", fine.is_paid)
            fine.date_paid = timezone.now()
            fine.save()
            print("saved fine: ", fine)
            return True
        except Fine.DoesNotExist:
            return False

    def can_borrow(self):
        unpaid_fines = self.get_total_unpaid_fines()
        if unpaid_fines > FINE_CAP:
            return False
        return True

    def __str__(self):
        return str(self.user_id)

class CurrentLoan(models.Model):
    customer = models.ForeignKey(LibraryCustomer, on_delete=models.CASCADE, related_name='current_loans')
    stock_item = models.ForeignKey('catalogue.StockItem', on_delete=models.CASCADE, related_name='current_loan')
    loan_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField() 
    class Meta:
        unique_together = ['customer', 'stock_item']  # Ensure a stock item isn't loaned to multiple customers
        ordering = ['-loan_date']

    def is_overdue(self):
        return timezone.now() > self.due_date

class LoanHistory(models.Model):
    customer = models.ForeignKey(LibraryCustomer, on_delete=models.CASCADE, related_name='loan_history')
    stock_item = models.ForeignKey('catalogue.StockItem', on_delete=models.CASCADE, related_name='loan_history')
    check_out_date = models.DateTimeField()
    return_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
        ('lost', 'Lost')
    ])

    class Meta:
        ordering = ['-check_out_date']

class Fine(models.Model):
    
    fine_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(LibraryCustomer, on_delete=models.CASCADE, related_name='fines')
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date_issued = models.DateTimeField(auto_now_add=True)
    loan_history = models.OneToOneField('LoanHistory', on_delete=models.CASCADE, related_name='fine')
    is_paid = models.BooleanField(default=False)
    date_paid = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.fine_id:
            self.fine_id = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Fine of £{self.amount} for {self.customer}"

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]

    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fine = models.ForeignKey(Fine, on_delete=models.CASCADE, related_name='payments')
    stripe_payment_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=PAYMENT_STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def amount(self):
        return self.fine.amount
    
    def __str__(self):
        return f"Payment {self.payment_id} for Fine {self.fine.fine_id}"

class PaymentHistory(models.Model):
    history_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='history')
    status_before = models.CharField(max_length=100)
    status_after = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Payment histories"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"History for Payment {self.payment.payment_id}"




