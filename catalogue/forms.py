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

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels, and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        self.fields['bib_num'].intial = self.instance.BibNum
        self.fields['title'].intial = self.instance.Title
        self.fields['author'].intial = self.instance.Author
        self.fields['publisher'].intial = self.instance.Publisher
        self.fields['publication_year'].intial = self.instance.PublicationYear
        self.fields['ISBN'].intial = self.instance.ISBN
        self.fields['subjects'].intial = self.instance.Subjects
        self.fields['item_type'].intial = self.instance.ItemType
        self.fields['item_collection'].intial = self.instance.ItemCollection
        self.fields['flaoting_item'].intial = self.instance.FloatingItem
        self.fields['item_location'].intial = self.instance.ItemLocation
        self.fields['report_date'].intial = self.instance.ReportDate
        self.fields['item_count'].intial = self.instance.ItemCount
