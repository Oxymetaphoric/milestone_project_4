# Generated by Django 5.1.2 on 2025-02-08 21:54

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_fine'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fine',
            name='id',
        ),
        migrations.AddField(
            model_name='fine',
            name='fine_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
