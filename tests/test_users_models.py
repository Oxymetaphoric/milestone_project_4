from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from catalogue.models import StockItem  # Assuming this exists
from users.models import (
    LibraryCustomer, CurrentLoan, LoanHistory, Fine, Payment, PaymentHistory
)
import uuid

class LibraryCustomerTest(TestCase):
    def setUp(self):
        print("Setting up LibraryCustomerTest")
        self.customer = LibraryCustomer.objects.create(
            first_name="John",
            last_name="Doe",
            street_address1="123 Main St",
            city_or_town="SampleTown",
            postcode="12345",
            phone_number="555-1234",
            email_address="john@example.com",
            is_child=False,
            date_of_birth="2000-01-01",
        )
    
    def test_auto_generated_user_id(self):
        print(f"Testing auto-generated user ID: {self.customer.user_id}")
        self.assertTrue(self.customer.user_id.startswith("A"))

    def test_get_total_unpaid_fines(self):
        Fine.objects.create(customer=self.customer, amount=Decimal('5.00'), loan_history=None)
        print(f"Total unpaid fines: {self.customer.get_total_unpaid_fines()}")
        self.assertEqual(self.customer.get_total_unpaid_fines(), Decimal('5.00'))
    
    def test_can_borrow(self):
        Fine.objects.create(customer=self.customer, amount=Decimal('11.00'), loan_history=None)
        print(f"Can borrow status: {self.customer.can_borrow()}")
        self.assertFalse(self.customer.can_borrow())

class CurrentLoanTest(TestCase):
    def setUp(self):
        print("Setting up CurrentLoanTest")
        self.customer = LibraryCustomer.objects.create(first_name="Alice", last_name="Smith", street_address1="456 Elm St",
            city_or_town="SampleCity", postcode="67890", phone_number="555-5678", email_address="alice@example.com",
            is_child=False, date_of_birth="1995-06-15")
        self.stock_item = StockItem.objects.create(stock_id="ST1234")
        self.loan = CurrentLoan.objects.create(customer=self.customer, stock_item=self.stock_item, due_date=timezone.now())
    
    def test_is_overdue(self):
        print(f"Loan due date: {self.loan.due_date}")
        self.assertFalse(self.loan.is_overdue())
        self.loan.due_date = timezone.now() - timezone.timedelta(days=1)
        print(f"Overdue check: {self.loan.is_overdue()}")
        self.assertTrue(self.loan.is_overdue())

class FineTest(TestCase):
    def setUp(self):
        print("Setting up FineTest")
        self.customer = LibraryCustomer.objects.create(first_name="Bob", last_name="Jones", street_address1="789 Pine Rd",
            city_or_town="TestCity", postcode="24680", phone_number="555-2468", email_address="bob@example.com",
            is_child=False, date_of_birth="1990-11-25")
        self.loan_history = LoanHistory.objects.create(customer=self.customer, stock_item=None, check_out_date=timezone.now(), return_date=timezone.now())
        self.fine = Fine.objects.create(customer=self.customer, amount=Decimal('15.00'), loan_history=self.loan_history)
    
    def test_fine_creation(self):
        print(f"Fine amount: {self.fine.amount}, Is paid: {self.fine.is_paid}")
        self.assertEqual(self.fine.amount, Decimal('15.00'))
        self.assertFalse(self.fine.is_paid)

class PaymentTest(TestCase):
    def setUp(self):
        print("Setting up PaymentTest")
        self.customer = LibraryCustomer.objects.create(first_name="Tom", last_name="Hardy", street_address1="101 Oak St",
            city_or_town="Nowhere", postcode="13579", phone_number="555-1357", email_address="tom@example.com",
            is_child=False, date_of_birth="1985-04-20")
        self.loan_history = LoanHistory.objects.create(customer=self.customer, stock_item=None, check_out_date=timezone.now(), return_date=timezone.now())
        self.fine = Fine.objects.create(customer=self.customer, amount=Decimal('8.00'), loan_history=self.loan_history)
        self.payment = Payment.objects.create(fine=self.fine, stripe_payment_id="stripe_123", status="PENDING")
    
    def test_payment_amount(self):
        print(f"Payment amount: {self.payment.amount}")
        self.assertEqual(self.payment.fine.amount, Decimal('8.00'))
        
    def test_payment_status_change(self):
        print(f"Old status: {self.payment.status}")
        self.payment.status = "COMPLETED"
        self.payment.save()
        print(f"New status: {self.payment.status}")
        self.assertEqual(self.payment.status, "COMPLETED")

class PaymentHistoryTest(TestCase):
    def setUp(self):
        print("Setting up PaymentHistoryTest")
        self.payment = Payment.objects.create(fine=None, stripe_payment_id="stripe_456", status="PENDING")
        self.payment_history = PaymentHistory.objects.create(payment=self.payment, status_before="PENDING", status_after="COMPLETED", timestamp=timezone.now())
    
    def test_payment_history_entry(self):
        print(f"Payment history: {self.payment_history.status_before} -> {self.payment_history.status_after}")
        self.assertEqual(self.payment_history.status_before, "PENDING")
        self.assertEqual(self.payment_history.status_after, "COMPLETED")
