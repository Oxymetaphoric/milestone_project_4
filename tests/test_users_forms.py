from django.test import TestCase, Client
from django.contrib.auth.models import User
from users.forms import CustomerForm 
from catalogue.models import CatalogueItem, StockItem
from users.models import LibraryCustomer 
import uuid

class CustomerFormTests(TestCase):
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

    def test_fields_placeholders_and_css_class(self):
        """
        Test that each field has the correct placeholder, CSS class,
        and that labels have been removed.
        """
        expected_placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email_address': 'Email Address',
            'phone_number': 'Phone Number',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'city_or_town': 'Town or City',
            'postcode': 'Postal Code',
            'date_of_birth': 'Date of Birth',
            'is_child': 'Is Child',
        }

        self.form = CustomerForm(instance=self.library_customer.user_id)
        for field_name, expected_placeholder in expected_placeholders.items():
            widget_attrs = self.form.fields[field_name].widget.attrs
            self.assertEqual(
                widget_attrs.get('placeholder'),
                expected_placeholder,
                msg=f"Placeholder for '{field_name}' should be '{expected_placeholder}'."
            )
            self.assertEqual(
                widget_attrs.get('class'),
                'stripe-style-input',
                msg=f"CSS class for '{field_name}' should be 'stripe-style-input'."
            )
            self.assertFalse(
                self.form.fields[field_name].label,
                msg=f"Label for '{field_name}' should be removed (False)."
            )

    def test_autofocus_on_first_field(self):
        """
        Test that the first field ('first_name') has the autofocus attribute.
        """
        autofocus_value = self.form.fields['first_name'].widget.attrs.get('autofocus', False)
        self.assertTrue(autofocus_value, msg="'first_name' should have autofocus set to True.")

    def test_crispy_helper_attributes(self):
        """
        Test that the form has a crispy forms helper with the expected attributes.
        """
        helper = self.form.helper
        self.assertIsInstance(helper, FormHelper)
        self.assertEqual(helper.form_id, 'edit-customer-form')
        self.assertEqual(helper.form_method, 'post')
        self.assertEqual(helper.form_enctype, 'multipart/form-data')

    def test_crispy_layout_structure(self):
        """
        Test that the crispy layout has the expected structure:
        - 5 Rows (each containing Columns)
        - 1 Div containing a Submit button.
        """
        layout = self.form.helper.layout
        # Expecting 6 elements in the layout
        self.assertEqual(len(layout), 6, msg="Layout should have 6 elements (5 Rows and 1 Div).")

        # First 5 elements should be Row instances
        for index in range(5):
            self.assertTrue(
                isinstance(layout[index], Row),
                msg=f"Element {index} in layout should be a Row instance."
            )

        # The 6th element should be a Div instance
        self.assertTrue(
            isinstance(layout[5], Div),
            msg="The last element in layout should be a Div instance."
        )
        # Check that the Div contains a Submit button by inspecting its string representation.
        # (This is a simplistic check; you may adjust it as needed.)
        self.assertIn('Submit', str(layout[5]),
                      msg="The Div in the layout should contain a Submit button.")

    def test_form_valid_with_valid_data(self):
        """
        Test that the form is valid when provided with valid data.
        """
        form = CustomerForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_text())

