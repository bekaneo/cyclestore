from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from django.core.mail import send_mail
from cycle import settings
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

    def send_notification(self, email, product_title):
        # TODO: change activations link
        message = f'Ваш продукт {product_title} пользователь {email} добавили в избранное '
        send_mail(subject='Добавили в избранное!',
                  message=message,
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[self.user],
                  fail_silently=False)

