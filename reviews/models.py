from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()


class LikedProduct(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='user', related_name='like')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name='product', related_name='like')


class CommentProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    text = models.CharField(max_length=240)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment')


class FavoriteProduct(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='user', related_name='favorite')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name='product', related_name='favorite')
