# Generated by Django 5.1.2 on 2025-02-02 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0015_alter_stockitem_status_loanitems'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanitems',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('overdue', 'Overdue'), ('maintenance', 'Maintenance'), ('discarded', 'Discarded'), ('missing', 'Missing')], max_length=20),
        ),
        migrations.AlterField(
            model_name='stockitem',
            name='Status',
            field=models.CharField(choices=[('available', 'Available'), ('overdue', 'Overdue'), ('maintenance', 'Maintenance'), ('discarded', 'Discarded'), ('missing', 'Missing')], max_length=20, null=True),
        ),
    ]
