# Generated by Django 5.1.2 on 2024-10-23 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_alter_stockitem_bibnum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockitem',
            name='PublicationYear',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='stockitem',
            name='ReportDate',
            field=models.CharField(max_length=256),
        ),
    ]