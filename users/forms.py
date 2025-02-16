from django import forms 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, ButtonHolder, Div
from .models import LibraryCustomer 

class CustomerForm(forms.ModelForm):
    class Meta:
        model = LibraryCustomer
        fields = [
            'first_name', 'last_name', 'email_address', 'phone_number', 
            'street_address1', 'street_address2', 'city_or_town', 
            'postcode', 'is_child', 'date_of_birth',
        ]
        
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels, and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
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
        
        self.helper = FormHelper()
        self.helper.form_id = 'edit-customer-form'
        self.helper.form_method = 'POST'
        self.helper.form_enctype = 'multipart/form-data'
        
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('street_address1', css_class='form-group col-md-6 mb-0'),
                Column('street_address2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('city_or_town', css_class='form-group col-md-6 mb-0'),
                Column('postcode', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email_address', css_class='form-group col-md-6 mb-0'),
                Column('phone_number', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('date_of_birth', css_class='form-group col-md-6 mb-0'),
                Column('is_child', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Div(
                Submit('submit', 'Save Changes', css_class='btn btn-primary'),
                css_class='form-group mt-3'
            )
        )
        
        for field in self.fields:
            placeholder = placeholders.get(field, '')
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
            
        # Autofocus on the first field
        self.fields['first_name'].widget.attrs['autofocus'] = True
