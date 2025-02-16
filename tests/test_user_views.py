from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import LibraryCustomer, Fine, LoanHistory, CurrentLoan
from decimal import Decimal
from django.utils import timezone
import uuid

class UsersViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        self.customer = LibraryCustomer.objects.create(
            user_id="A0000001",
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

        self.fine = Fine.objects.create(
            fine_id=uuid.uuid4(),
            customer=self.customer,
            amount=Decimal('5.00'),
            date_issued=timezone.now(),
            is_paid=False
        )

        self.loan = CurrentLoan.objects.create(
            customer=self.customer,
            stock_item=None,
            due_date=timezone.now()
        )

        self.loan_history = LoanHistory.objects.create(
            customer=self.customer,
            stock_item=None,
            check_out_date=timezone.now(),
            return_date=timezone.now(),
            status='completed'
        )
    
    def test_find_users_view(self):
        response = self.client.get(reverse('find_users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/users_home.html')
    
    def test_search_users_view(self):
        response = self.client.get(reverse('search_users'), {'q': 'John'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John")
    
    def test_display_customer_details_view(self):
        response = self.client.get(reverse('display_customer_details', args=[self.customer.user_id]))
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
        response = self.client.post(reverse('edit_library_customer', args=[self.customer.user_id]), {
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
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.first_name, 'Johnny')
    
    def test_delete_library_customer_view(self):
        response = self.client.post(reverse('delete_library_customer', args=[self.customer.user_id]))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(LibraryCustomer.DoesNotExist):
            LibraryCustomer.objects.get(user_id=self.customer.user_id)
    
    def test_customer_loan_history_view(self):
        response = self.client.get(reverse('customer_loan_history', args=[self.customer.user_id]))
        self.assertEqual(response.status_code, 200)
    
    def test_payment_page_view(self):
        response = self.client.get(reverse('payment_page', args=[self.fine.fine_id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '£5.00')

