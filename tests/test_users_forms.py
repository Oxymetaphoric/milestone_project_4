from django.test import TestCase
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Submit
from users.forms import CustomerForm


class CustomerFormTests(TestCase):
    def setUp(self):
        self.form = CustomerForm()
        self.valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email_address': 'john.doe@example.com',
            'phone_number': '1234567890',
            'street_address1': '123 Main St',
            'street_address2': 'Apt 4B',
            'city_or_town': 'Anytown',
            'postcode': '12345',
            'is_child': False,
            'date_of_birth': '2000-01-01',
        }

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

