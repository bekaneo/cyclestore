# Generated by Django 4.0.5 on 2022-07-18 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('brand', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('size_in_inch', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('size_in_cm', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100, primary_key=True, serialize=False)),
            ],
        ),
    ]
