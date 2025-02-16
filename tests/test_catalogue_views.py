from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from catalogue.models import CatalogueItem, StockItem
from users.models import LibraryCustomer, CurrentLoan, LoanHistory, Fine
from django.utils import timezone
from datetime import timedelta
import uuid


class CatalogueViewsTests(TestCase):
    def setUp(self):
        # Create a test user (librarian) for authentication
        self.user = User.objects.create_user(username='testuser', password='loginrequired')
        # Log in with the User (the librarian who manages LibraryCustomers)
        self.client = Client()
        self.client.login(username='testuser', password='loginrequired')
        # Create a test library customer (a separate entity representing a customer)
        self.library_customer = LibraryCustomer.objects.create(
            user_id='A0000005',  
            email_address='test@customer.com',
            first_name = 'John', 
            last_name = 'Doe',
            street_address1 = '12 No Street',
            street_address2 = '',
            city_or_town = 'nowhere',
            postcode = 'AA1A33',
            phone_number = '1234567890',
            is_child = 'False',
            date_of_birth = '1980-06-12'
        )

        self.library_customer.user = self.user
        self.library_customer.save()

        # Create a test catalogue item
        self.catalogue_item = CatalogueItem.objects.create(
            BibNum = '123456', 
            Title = 'Test Book',
            Author = 'Test Author',
            ISBN = '123556789',
            PublicationYear = '2009',
            Publisher = 'Test Publisher',
            Subjects = 'test',
            ItemType = 'test',
            ItemCollection = 'test',
            FloatingItem = 'test',
            ItemLocation = 'test',
            ReportDate = 'test',
            ItemCount = '5'

        )

        # Create a test stock item
        self.stock_item = StockItem.objects.create(
            StockID=uuid.uuid4(),
            catalogue_item=self.catalogue_item,
            Status='available',
            Location='In Branch',
            Borrower = self.library_customer,
            last_updated = '01/01/2001'

        )

    def test_display_catalogue_items(self):
        """
        Test that the catalogue items are displayed correctly.
        """
        response = self.client.get(reverse('display_catalogue_items'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')
        self.assertContains(response, 'Test Author')
        self.assertContains(response, 'Test Publisher')

    def test_search_catalogue(self):
        """
        Test that the search functionality returns the correct results.
        """
        response = self.client.get(reverse('search_catalogue'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        # Parse JSON response
        data = response.json()
        self.assertTrue(any(item['Title'] == 'Test Book' for item in data))
        self.assertTrue(any(item['Author'] == 'Test Author' for item in data))
        self.assertTrue(any(item['Publisher'] == 'Test Publisher' for item in data))

    def test_book_info_get(self):
        """
        Test that the book info page is displayed correctly for a GET request.
        """
        response = self.client.get(reverse('book_info', args=[self.catalogue_item.BibNum]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')
        self.assertContains(response, str(self.stock_item.StockID))

    def test_book_info_post_add_copies(self):
        """
        Test that adding copies to a book works correctly.
        """
        response = self.client.post(
            reverse('book_info', args=[self.catalogue_item.BibNum]),
            {
                'add_copies': 'True',
                'quantity': '2'
            }
        )
        self.assertEqual(response.status_code, 302)  # Expect a redirect after POST
        # Initially there was one copy, so adding 2 should result in 3 total
        self.assertEqual(StockItem.objects.filter(catalogue_item=self.catalogue_item).count(), 3)

    def test_book_info_post_delete_stock_item(self):
        """
        Test that deleting a stock item works correctly.
        """
        response = self.client.post(
            reverse('book_info', args=[self.catalogue_item.BibNum]),
            {
                'delete_stock_item': 'True',
                'stock_id': str(self.stock_item.StockID)
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirect expected
        self.assertEqual(StockItem.objects.filter(catalogue_item=self.catalogue_item).count(), 0)

    def test_book_info_post_update_stock_item(self):
        """
        Test that updating a stock item's status works correctly.
        """
        response = self.client.post(
            reverse('book_info', args=[self.catalogue_item.BibNum]),
            {
                'update_stock_item': 'True',
                'stock_id': str(self.stock_item.StockID),
                'status': 'on_loan'
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirect expected
        updated_stock_item = StockItem.objects.get(StockID=self.stock_item.StockID)
        self.assertEqual(updated_stock_item.Status, 'on_loan')

    def test_check_out(self):
        """
        Test that checking out a book works correctly.
        """
        response = self.client.post(
            reverse('check_out'),
            {
                'stock_id': str(self.stock_item.StockID),
                'user_id': self.library_customer.user_id
            }
        )
        self.assertEqual(response.status_code, 200)
        updated_stock_item = StockItem.objects.get(StockID=self.stock_item.StockID)
        self.assertEqual(updated_stock_item.Status, 'on_loan')
        self.assertEqual(updated_stock_item.Borrower, self.customer.user_id)
        self.assertTrue(CurrentLoan.objects.filter(stock_item=self.stock_item).exists())

    def test_check_in(self):
        """
        Test that checking in a book works correctly.
        """
        # First, check out the book
        self.client.post(
            reverse('check_out'),
            {
                'stock_id': str(self.stock_item.StockID),
                'user_id': self.library_customer.user_id
            }
        )

        # Then, check it in
        response = self.client.post(
            reverse('check_in'),
            {
                'stock_id': str(self.stock_item.StockID)
            }
        )
        self.assertEqual(response.status_code, 200)
        updated_stock_item = StockItem.objects.get(StockID=self.stock_item.StockID)
        self.assertEqual(updated_stock_item.Status, 'available')
        self.assertEqual(updated_stock_item.Location, 'In Branch')
        self.assertIsNone(updated_stock_item.Borrower)
        self.assertTrue(LoanHistory.objects.filter(stock_item=self.stock_item).exists())

    def test_lost_item(self):
        """
        Test that marking a book as lost works correctly.
        """
        # First, check out the book
        self.client.post(
            reverse('check_out'),
            {
                'stock_id': str(self.stock_item.StockID),
                'user_id': self.library_customer.user_id
            }
        )

        # Then, mark it as lost
        response = self.client.post(
            reverse('lost_item'),
            {
                'stock_id': str(self.stock_item.StockID),
                'user_id': self.library_customer.user_id
            }
        )
        self.assertEqual(response.status_code, 302)  # Expect a redirect after POST
        updated_stock_item = StockItem.objects.get(StockID=self.stock_item.StockID)
        self.assertEqual(updated_stock_item.Status, 'missing')
        self.assertEqual(updated_stock_item.Location, 'missing')
        self.assertIsNone(updated_stock_item.Borrower)
        # Check that a fine of LOST_ITEM (10.00) has been created
        self.assertTrue(Fine.objects.filter(customer=self.library_customer, amount=10.00).exists())

