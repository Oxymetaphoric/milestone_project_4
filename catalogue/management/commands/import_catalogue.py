import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from catalogue.models import CatalogueItem

class Command(BaseCommand):
    help = 'Import catalogue data from CSV file with duplicate handling'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')
        parser.add_argument(
            '--update-existing', 
            action='store_true', 
            help='Update existing records instead of skipping'
        )

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        update_existing = options['update_existing']

        try:
            with pd.read_csv(csv_file_path, chunksize=1000) as csv_reader:
                for chunk in csv_reader:
                    # Remove duplicates within the chunk, keeping the first occurrence
                    chunk = chunk.drop_duplicates(subset='BibNum', keep='first')

                    # Get existing BibNums to filter out duplicates
                    existing_bibnums = set(
                        CatalogueItem.objects.filter(
                            BibNum__in=chunk['BibNum'].tolist()
                        ).values_list('BibNum', flat=True)
                    )

                    catalogue_items = []
                    for _, row in chunk.iterrows():
                        # Skip or update based on existing records
                        if row['BibNum'] not in existing_bibnums:
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
                        elif update_existing:
                            # Optional: Update existing records if flag is set
                            try:
                                existing_item = CatalogueItem.objects.get(BibNum=row['BibNum'])
                                existing_item.Title = row['Title']
                                existing_item.Author = row['Author']
                                # Update other fields as needed
                                existing_item.save()
                            except CatalogueItem.DoesNotExist:
                                pass

                    # Bulk create new items
                    if catalogue_items:
                        try:
                            with transaction.atomic():
                                CatalogueItem.objects.bulk_create(catalogue_items)
                                self.stdout.write(
                                    self.style.SUCCESS(f'Imported {len(catalogue_items)} new records')
                                )
                        except Exception as e:
                            self.stdout.write(
                                self.style.ERROR(f'Error importing chunk. Error: {str(e)}')
                            )

            self.stdout.write(self.style.SUCCESS('Catalogue data import completed'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file_path}'))
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.ERROR('CSV file is empty or has invalid data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {str(e)}'))
