from django.contrib.auth import get_user_model
from django.db import models

from categories.models import Category, Brand

User = get_user_model()

COLORS = [
    ('black', 'black'),
    ('white', 'white'),
    ('red', 'red'),
    ('blue', 'blue')
]

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='subcategory')
    color = models.CharField(max_length=20, choices=COLORS)
    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
