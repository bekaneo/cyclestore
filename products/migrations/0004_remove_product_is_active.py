# Generated by Django 4.0.5 on 2022-07-20 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_active',
        ),
    ]
