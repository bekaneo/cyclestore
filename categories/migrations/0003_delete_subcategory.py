# Generated by Django 4.0.5 on 2022-07-12 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_product_subcategory_product_brand'),
        ('categories', '0002_brand_size_remove_subcategory_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SubCategory',
        ),
    ]
