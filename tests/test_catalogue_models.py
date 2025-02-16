import uuid
from django.test import TestCase
from catalogue.models import CatalogueItem, StockItem

class CatalogueItemModelTest(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.catalogue_item = CatalogueItem.objects.create(
            BibNum='B12345',
            Title='Test Book Title',
            Author='Test Author',
            ISBN='1234567890',
            PublicationYear='2020',
            Publisher='Test Publisher',
            Subjects='Fiction, Test',
            ItemType='Book',
            ItemCollection='General',
            FloatingItem='Yes',
            ItemLocation='Main Library',
            ReportDate='2023-01-01',
            ItemCount=0
        )
    
    def test_catalogue_item_creation(self):
        """Test that a catalogue item can be created with valid data"""
        self.assertEqual(self.catalogue_item.BibNum, 'B12345')
        self.assertEqual(self.catalogue_item.Title, 'Test Book Title')
        self.assertEqual(self.catalogue_item.Author, 'Test Author')
        self.assertEqual(self.catalogue_item.ItemType, 'Book')
        self.assertEqual(self.catalogue_item.ItemCount, 0)
    
    def test_string_representation(self):
        """Test the string representation of the catalogue item"""
        self.assertEqual(str(self.catalogue_item), 'Test Book Title')
    
    def test_optional_fields(self):
        """Test that optional fields can be null/blank"""
        optional_item = CatalogueItem.objects.create(
            BibNum='B67890',
            Title='Optional Fields Test',
            Author='Optional Author',
            Publisher='Optional Publisher',
            Subjects='Optional',
            ItemType='Book',
            ItemCollection='General',
            ItemLocation='Branch',
            ReportDate='2023-02-01'
        )
        self.assertIsNone(optional_item.ISBN)
        self.assertIsNone(optional_item.PublicationYear)
        self.assertIsNone(optional_item.FloatingItem)
        
    def test_update_item_count(self):
        """Test that update_item_count updates the count correctly"""
        # First, verify initial count is 0
        self.assertEqual(self.catalogue_item.ItemCount, 0)
        
        # Create some mock stock items linked to this catalogue item
        # Assuming StockItem has a ForeignKey to CatalogueItem named 'catalogue_item'
        StockItem.objects.create(
            catalogue_item=self.catalogue_item,
            Status='Available'  # This is required based on your model
        )
        StockItem.objects.create(
            catalogue_item=self.catalogue_item,
            Status='Available'  # This is required based on your model
        )
        
        # Run the update method
        self.catalogue_item.update_item_count()
        
        # Verify the count was updated
        self.assertEqual(self.catalogue_item.ItemCount, 2)
        
        # Verify the change persisted to the database
        refreshed_item = CatalogueItem.objects.get(BibNum='B12345')
        self.assertEqual(refreshed_item.ItemCount, 2)
    
    def test_bibnum_as_primary_key(self):
        """Test that BibNum works correctly as a primary key"""
        # Try to get the item by primary key
        retrieved_item = CatalogueItem.objects.get(pk='B12345')
        self.assertEqual(retrieved_item, self.catalogue_item)
        
        # Test that we can't create another item with the same BibNum
        with self.assertRaises(Exception):
            CatalogueItem.objects.create(
                BibNum='B12345',  # Same as existing item
                Title='Duplicate BibNum Test',
                Author='Another Author',
                Publisher='Another Publisher',
                Subjects='Another Subject',
                ItemType='Book',
                ItemCollection='General',
                ItemLocation='Branch',
                ReportDate='2023-03-01'
            )

class StockItemModelTest(TestCase):
    
    def setUp(self):
        """Set up test data"""
        # Create a catalogue item first
        self.catalogue_item = CatalogueItem.objects.create(
            BibNum='B12345',
            Title='Test Book Title',
            Author='Test Author',
            ISBN='1234567890',
            PublicationYear='2020',
            Publisher='Test Publisher',
            Subjects='Fiction, Test',
            ItemType='Book',
            ItemCollection='General',
            FloatingItem='Yes',
            ItemLocation='Main Library',
            ReportDate='2023-01-01',
            ItemCount=0
        )
        
        # Now create a stock item
        self.stock_item = StockItem.objects.create(
            Status='Available',
            Location='Shelf A1',
            catalogue_item=self.catalogue_item
        )
    
    def test_stock_item_creation(self):
        """Test that a stock item can be created with valid data"""
        self.assertIsInstance(self.stock_item.StockID, uuid.UUID)
        self.assertEqual(self.stock_item.Status, 'Available')
        self.assertEqual(self.stock_item.Location, 'Shelf A1')
        self.assertIsNone(self.stock_item.Borrower)
        self.assertEqual(self.stock_item.catalogue_item, self.catalogue_item)
    
    def test_string_representation(self):
        """Test the string representation of the stock item"""
        self.assertEqual(str(self.stock_item), str(self.stock_item.StockID))
    
    def test_catalogue_item_relationship(self):
        """Test the relationship with CatalogueItem"""
        # Test that the stock item is in the catalogue item's related items
        self.assertIn(self.stock_item, self.catalogue_item.stock_items.all())
        
        # Test that deletion cascades properly
        catalogue_item_bibnum = self.catalogue_item.BibNum
        self.catalogue_item.delete()
        with self.assertRaises(StockItem.DoesNotExist):
            StockItem.objects.get(pk=self.stock_item.StockID)
    
    def test_properties(self):
        """Test that properties correctly return catalogue item attributes"""
        self.assertEqual(self.stock_item.BibNum, self.catalogue_item.BibNum)
        self.assertEqual(self.stock_item.Title, self.catalogue_item.Title)
        self.assertEqual(self.stock_item.Author, self.catalogue_item.Author)
        self.assertEqual(self.stock_item.ISBN, self.catalogue_item.ISBN)
        self.assertEqual(self.stock_item.PublicationYear, self.catalogue_item.PublicationYear)
        self.assertEqual(self.stock_item.Publisher, self.catalogue_item.Publisher)
        self.assertEqual(self.stock_item.Subjects, self.catalogue_item.Subjects)
        self.assertEqual(self.stock_item.ItemType, self.catalogue_item.ItemCollection)  # Note: this maps to ItemCollection
        self.assertEqual(self.stock_item.FloatingItem, self.catalogue_item.FloatingItem)
        self.assertEqual(self.stock_item.ItemLocation, self.catalogue_item.ItemLocation)
        self.assertEqual(self.stock_item.ReportDate, self.catalogue_item.ReportDate)
        self.assertEqual(self.stock_item.ItemCount, self.catalogue_item.ItemCount)
        self.assertEqual(self.stock_item.ItemCollection, self.catalogue_item.ItemCollection)
    
    def test_update_catalogue_item_count_signal(self):
        """Test that the signal updates the catalogue item count"""
        # Initial count should be 1 after setUp
        self.catalogue_item.refresh_from_db()
        self.assertEqual(self.catalogue_item.ItemCount, 1)
        
        # Add another stock item
        new_stock_item = StockItem.objects.create(
            Status='Available',
            Location='Shelf A2',
            catalogue_item=self.catalogue_item
        )
        
        # Count should be updated to 2
        self.catalogue_item.refresh_from_db()
        self.assertEqual(self.catalogue_item.ItemCount, 2)
        
        # Delete one stock item
        new_stock_item.delete()
        
        # Count should be updated to 1
        self.catalogue_item.refresh_from_db()
        self.assertEqual(self.catalogue_item.ItemCount, 1)
    
    def test_optional_fields(self):
        """Test that optional fields can be null/blank"""
        stock_item = StockItem.objects.create(
            catalogue_item=self.catalogue_item,
            Status='Available'
        )
        self.assertIsNone(stock_item.Location)
        self.assertIsNone(stock_item.Borrower)

    def test_current_loan_property(self):
        """Test the current_loan property"""
        # Without mocking CurrentLoan, we just test that it doesn't error
        self.assertIsNone(self.stock_item.current_loan)
