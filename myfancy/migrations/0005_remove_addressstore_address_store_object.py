# Generated by Django 5.0.6 on 2024-10-19 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myfancy', '0004_addressstore'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addressstore',
            name='address_store_object',
        ),
    ]
