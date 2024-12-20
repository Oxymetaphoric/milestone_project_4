# Generated by Django 5.1.2 on 2024-11-01 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0009_alter_catalogueitem_floatingitem_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogueitem',
            name='Author',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='catalogueitem',
            name='FloatingItem',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='catalogueitem',
            name='ISBN',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='catalogueitem',
            name='PublicationYear',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='catalogueitem',
            name='Publisher',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='catalogueitem',
            name='ReportDate',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='catalogueitem',
            name='Subjects',
            field=models.CharField(max_length=1024),
        ),
    ]
