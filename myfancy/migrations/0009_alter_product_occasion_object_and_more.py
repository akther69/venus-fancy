# Generated by Django 5.0.6 on 2024-09-01 16:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfancy', '0008_alter_product_type_object'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='occasion_object',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='myfancy.occasion'),
        ),
        migrations.AlterField(
            model_name='product',
            name='type_object',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='myfancy.type'),
        ),
    ]
