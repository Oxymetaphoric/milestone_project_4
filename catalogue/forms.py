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
        labels = {
                'BibNum': 'Bibliographic Number',
                'Title': 'Title',
                'Author': 'Author',
                'Publisher': 'Publisher',
                'PublicationYear': 'Year of Publication',
                'ISBN': 'ISBN',
                'Subjects': 'Subjects',
                'ItemType': 'Item Type',
                'ItemCollection': 'Item Collection',
                'FloatingItem': 'Floating Item',
                'ItemLocation': 'Item Location',
                'ReportDate': 'Report Date',
                'ItemCount': 'Item Count',

                }

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels, and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'BibNum': 'Bibliographic Number:',
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
        self.fields['BibNum'].widget.attrs['autofocus'] = True

class StockForm(forms.ModelForm):
    bib_num = forms.CharField(disabled=True, required=False)
    title = forms.CharField(disabled=True, required=False)
    author = forms.CharField(disabled=True, required=False)
    publisher = forms.CharField(disabled=True, required=False)
    publication_year = forms.CharField(disabled=True, required=False)
    ISBN = forms.CharField(disabled=True, required=False)
    subjects = forms.CharField(disabled=True, required=False)
    item_type = forms.CharField(disabled=True, required=False)
    item_collection = forms.CharField(disabled=True, required=False)
    floating_item = forms.CharField(disabled=True, required=False)
    item_location = forms.CharField(disabled=True, required=False)
    report_date = forms.CharField(disabled=True, required=False)
    item_count = forms.IntegerField(required=False)

    class Meta:
        model = StockItem
        fields = [
                'item_count',
                    ]
        labels = {
                'bib_num': 'Bibliographic Number:',
                'title': 'Title:',
                'author': 'Author:',
                'publisher': 'Publisher:',
                'publication_year': 'Year of Publication:',
                'ISBN': 'ISBN:',
                'subjects': 'Subjects:',
                'item_type': 'Item Type:',
                'item_collection': 'Item Collection:',
                'floating_item': 'Floating Item:',
                'item_location': 'Item Location:',
                'report_date': 'Report Date:',
                'item_count': 'Item Count:',

                }

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels, and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        self.fields['bib_num'].initial = self.instance.BibNum
        self.fields['title'].initial = self.instance.Title
        self.fields['author'].initial = self.instance.Author
        self.fields['publisher'].initial = self.instance.Publisher
        self.fields['publication_year'].initial = self.instance.PublicationYear
        self.fields['ISBN'].initial = self.instance.ISBN
        self.fields['subjects'].initial = self.instance.Subjects
        self.fields['item_type'].initial = self.instance.ItemType
        self.fields['item_collection'].initial = self.instance.ItemCollection
        self.fields['floating_item'].initial = self.instance.FloatingItem
        self.fields['item_location'].initial = self.instance.ItemLocation
        self.fields['report_date'].initial = self.instance.ReportDate
        self.fields['item_count'].initial = self.instance.ItemCount
