# Generated by Django 5.1.2 on 2024-10-27 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryCustomer',
            fields=[
                ('user_id', models.CharField(blank=True, max_length=8, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=256, null=True)),
                ('last_name', models.CharField(max_length=256)),
                ('street_address1', models.CharField(max_length=256)),
                ('street_address2', models.CharField(blank=True, max_length=256, null=True)),
                ('city_or_town', models.CharField(max_length=256)),
                ('postcode', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=25)),
                ('email_address', models.CharField(max_length=256)),
                ('is_child', models.BooleanField()),
                ('date_of_birth', models.DateField()),
            ],
        ),
    ]
