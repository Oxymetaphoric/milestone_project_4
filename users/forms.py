from django import forms
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

        for field in self.fields:
            placeholder = placeholders.get(field, '')
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False        # Autofocus on the first field
        self.fields['first_name'].widget.attrs['autofocus'] = True

