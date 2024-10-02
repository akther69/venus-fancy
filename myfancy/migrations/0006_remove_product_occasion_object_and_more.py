# Generated by Django 5.0.6 on 2024-09-01 16:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfancy', '0005_remove_product_occasion_object_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='occasion_object',
        ),
        migrations.RemoveField(
            model_name='product',
            name='type_object',
        ),
        migrations.AddField(
            model_name='product',
            name='occasion_object',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myfancy.occasion'),
        ),
        migrations.AddField(
            model_name='product',
            name='type_object',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myfancy.type'),
        ),
    ]
