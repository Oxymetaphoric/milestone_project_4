import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from catalogue.models import CatalogueItem  

class Command(BaseCommand):
    help = 'Import catalogue data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        # Open the CSV file in chunks to handle large file sizes
        try:
            with pd.read_csv(csv_file_path, chunksize=1000) as csv_reader:
                for chunk in csv_reader:
                    catalogue_items = []

                    # Iterate over each row in the chunk
                    for _, row in chunk.iterrows():
                        # Append each row as a StockItem instance to the list
                        catalogue_items.append(CatalogueItem(
                            BibNum=row['BibNum'],
                            Title=row['Title'],
                            Author=row['Author'],
                            ISBN=row['ISBN'],
                            PublicationYear=row['PublicationYear'],
                            Publisher=row['Publisher'],
                            Subjects=row['Subjects'],
                            ItemType=row['ItemType'],
                            ItemCollection=row['ItemCollection'],
                            FloatingItem=row['FloatingItem'],
                            ItemLocation=row['ItemLocation'],
                            ReportDate=row['ReportDate'],
                            ItemCount=row['ItemCount'],
                        ))

                    # Use bulk_create to insert the data in a single transaction
                    try:
                        with transaction.atomic():
                            CatalogueItem.objects.bulk_create(catalogue_items)
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'Error importing chunk. Error: {str(e)}')
                        )

            self.stdout.write(self.style.SUCCESS('Successfully imported catalogue data'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file_path}'))
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.ERROR('CSV file is empty or has invalid data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {str(e)}'))

