# Generated by Django 4.0.5 on 2022-07-19 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_product_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='views',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
