# Generated by Django 5.1.2 on 2024-10-26 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0005_delete_stockitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalogueitem',
            name='id',
            field=models.BigAutoField(auto_created=True, default=2, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='catalogueitem',
            name='BibNum',
            field=models.CharField(max_length=256),
        ),
    ]