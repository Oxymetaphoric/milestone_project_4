# Generated by Django 5.1.2 on 2024-10-27 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0006_catalogueitem_id_alter_catalogueitem_bibnum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalogueitem',
            name='id',
        ),
        migrations.AlterField(
            model_name='catalogueitem',
            name='BibNum',
            field=models.CharField(max_length=256, primary_key=True, serialize=False),
        ),
    ]