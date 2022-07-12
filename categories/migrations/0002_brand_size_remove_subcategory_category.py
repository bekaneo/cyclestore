# Generated by Django 4.0.5 on 2022-07-12 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size_in_inch', models.CharField(max_length=10)),
                ('size_in_cm', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='category',
        ),
    ]