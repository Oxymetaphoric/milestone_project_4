from django import forms
from .models import CatalogueItem, StockItem

class CatalogueForm(forms.ModelForm):
    class Meta:
        model = CatalogueItem
        fields = [
                'BibNum', 'Title', 'Author',
                'Publisher', 'PublicationYear', 'ISBN',
                'Subjects', 'ItemType', 'ItemCollection',
                'FloatingItem', 'ItemLocation', 'ReportDate',
                'ItemCount',
                    ]

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels, and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'BibNum': 'Bibliographic Number',
            'Title': 'Title',
            'Author': 'Author',
            'Publisher': 'Publisher',
            'PublicationYear': 'Publication Year',
            'ISBN': 'ISBN',
            'Subjects': 'Subjects',
            'ItemType': 'Item Type',
            'ItemCollection': 'Item Collection',
            'FloatingItem': 'Floating Item?',
            'ItemLocation': 'Item Location',
            'ReportDate': 'Report Date',
            'ItemCount': 'Item Count',
        }

        for field in self.fields:
            placeholder = placeholders.get(field, '')
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False        # Autofocus on the first field
        self.fields['first_name'].widget.attrs['autofocus'] = True

class StockForm(forms.ModelForm):
    class Meta:
        model = StockItem
        fields = [
                'catalogue_item',
                    ]

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels, and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
                'catalogue_item': 'Catalogue entry',
                    }

        for field in self.fields:
            placeholder = placeholders.get(field, '')
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False        # Autofocus on the first field

