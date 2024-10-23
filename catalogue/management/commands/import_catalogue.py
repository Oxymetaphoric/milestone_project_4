'''
catalogue/
    management/
        __init__.py
        commands/
            __init__.py
            import_catalogue.py


Then put this code in `import_catalogue.py`:

'''

import csv
from django.core.management.base import BaseCommand
from catalogue.models import StockItem  # Replace with your actual model name

class Command(BaseCommand):
    help = 'Import catalogue data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Create a model instance for each row
                    # Replace the field names with your actual model field names
                    StockItem.objects.create(
                        BibNum=row['csv_column1'],
                        Title=row['csv_column2'],
                        Author=row['csv_column3'],
                        ISBN=row['csv_column4'],
                        PublicationYear=row['csv_column5'],
                        Publisher=row['csv_column6'],
                        Subjects=row['csv_column7'],
                        ItemType=row['csv_column8'],
                        ItemCollection=row['csv_column9'],
                        FloatingItem=row['csv_column10'],
                        ItemLocation=row['csv_column11'],
                        ReportDate=row['csv_column12'],
                        ItemCount=row['csv_column13'],
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error importing row: {row}. Error: {str(e)}')
                    )

        self.stdout.write(
            self.style.SUCCESS('Successfully imported catalogue data')
        )

'''

To use this command:

1. First, update the import statement to import your actual model:

from catalogue.models import YourModel  # Replace YourModel with your actual model name


2. Update the field mappings in the `YourModel.objects.create()` call to match your model fields and CSV columns.

3. Then run the command:

python manage.py import_catalogue path/to/your/csv/file.csv
'''

