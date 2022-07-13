from django.contrib.auth import get_user_model
from django.db import models

from products.models import Product

User = get_user_model()

STATUS_CHOICES = (
    ('open', 'Open'),
    ('in_process', 'In Process'),
    ('canceled', 'Canceled'),
    ('finished', 'Finished')
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=100, blank=True)
    products = models.ManyToManyField(Product, through='OrderItems')
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='open')

    def str(self):
        return f'Order #{self.id}'


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.PositiveSmallIntegerField(default=1)

# dfs