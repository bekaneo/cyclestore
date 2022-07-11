from django.contrib.auth import get_user_model
from django.db import models
from categories.models import Category, SubCategory

User = get_user_model()


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products')

    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='subcategory')

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
