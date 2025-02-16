from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import LibraryCustomer, Fine, LoanHistory, CurrentLoan
from catalogue.models import CatalogueItem, StockItem
from decimal import Decimal
from django.utils import timezone
import uuid

class UsersViewsTest(TestCase):
    def setUp(self):
        # Create a test user (librarian) for authentication
        self.user = User.objects.create_user(username='testuser', password='loginrequired')
        # Log in with the User (the librarian who manages LibraryCustomers)
        self.client = Client()
        self.client.login(username='testuser', password='loginrequired')
        
        # Create a test library customer
        self.library_customer = LibraryCustomer.objects.create(
            user_id='A0000005',  
            email_address='test@customer.com',
            first_name='John', 
            last_name='Doe',
            street_address1='12 No Street',
            street_address2='',
            city_or_town='nowhere',
            postcode='AA1A33',
            phone_number='1234567890',
            is_child=False,  # Use boolean, not string
            date_of_birth='1980-06-12'
        )

        # Create a test catalogue item
        self.catalogue_item = CatalogueItem.objects.create(
            BibNum='123456', 
            Title='Test Book',
            Author='Test Author',
            ISBN='123556789',
            PublicationYear='2009',
            Publisher='Test Publisher',
            Subjects='test',
            ItemType='test',
            ItemCollection='test',
            FloatingItem='test',
            ItemLocation='test',
            ReportDate='test',
            ItemCount=5  # Use integer, not string
        )

        # Create a test stock item
        self.stock_item = StockItem.objects.create(
            StockID=uuid.uuid4(),
            catalogue_item=self.catalogue_item,
            Status='available',
            Location='In Branch',
            Borrower=self.library_customer,
            last_updated='2001-01-01'  # Use valid date format
        )

        # Create a loan history for the customer
        self.loan_history = LoanHistory.objects.create(
            customer=self.library_customer,
            stock_item=self.stock_item,
            check_out_date=timezone.now(),
            return_date=timezone.now(),
            status='completed'
        )

        # Create a fine for the customer and link it to the loan history
        self.fine = Fine.objects.create(
            fine_id=uuid.uuid4(),
            customer=self.library_customer,
            loan_history=self.loan_history,  # Link to the loan history
            amount=Decimal('5.00'),
            date_issued=timezone.now(),
            is_paid=False
        )

        # Create a current loan for the customer
        self.current_loan = CurrentLoan.objects.create(
            customer=self.library_customer,
            stock_item=self.stock_item,
            due_date=timezone.now()
        )
    
    def test_display_customer_details_view(self):
        response = self.client.get(reverse('display_customer_details', args=[self.library_customer.user_id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John")

    def test_add_library_customer_view(self):
        response = self.client.post(reverse('add_library_customer'), {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'street_address1': '456 Elm St',
            'city_or_town': 'New Town',
            'postcode': '67890',
            'phone_number': '555-6789',
            'email_address': 'alice@example.com',
            'is_child': False,
            'date_of_birth': '1995-06-15',
        })
        self.assertEqual(response.status_code, 302)

    def test_edit_library_customer_view(self):
        response = self.client.post(reverse('edit_library_customer', args=[self.library_customer.user_id]), {
            'first_name': 'Johnny',
            'last_name': 'Doe',
            'street_address1': '123 Main St',
            'city_or_town': 'SampleTown',
            'postcode': '12345',
            'phone_number': '555-1234',
            'email_address': 'john@example.com',
            'is_child': False,
            'date_of_birth': '2000-01-01',
        })
        self.assertEqual(response.status_code, 302)
        self.library_customer.refresh_from_db()
        self.assertEqual(self.library_customer.first_name, 'Johnny')

    def test_delete_library_customer_view(self):
        response = self.client.post(reverse('delete_library_customer', args=[self.library_customer.user_id]))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(LibraryCustomer.DoesNotExist):
            LibraryCustomer.objects.get(user_id=self.library_customer.user_id)

    def test_customer_loan_history_view(self):
        response = self.client.get(reverse('customer_loan_history', args=[self.library_customer.user_id]))
        self.assertEqual(response.status_code, 200)

    def test_payment_page_view(self):
        response = self.client.get(reverse('payment_page', args=[self.fine.fine_id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '£5.00')
