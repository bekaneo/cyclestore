# Generated by Django 4.0.5 on 2022-07-18 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='size',
            old_name='size_in_inch',
            new_name='inch',
        ),
        migrations.RemoveField(
            model_name='size',
            name='size_in_cm',
        ),
    ]