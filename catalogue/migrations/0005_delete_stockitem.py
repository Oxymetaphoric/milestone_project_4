# Generated by Django 5.1.2 on 2024-10-26 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0004_remove_stockitem_id_alter_stockitem_stockid'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StockItem',
        ),
    ]