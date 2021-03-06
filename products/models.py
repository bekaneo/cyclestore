from categories.models import Type, Brand, Size
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Type,
                                 on_delete=models.CASCADE,
                                 related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='subcategory')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='size', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
