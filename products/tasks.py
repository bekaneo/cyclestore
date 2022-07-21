from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_notification(user, title, author, desc):
    send_mail(
        subject='Added to favorites',
        message=f'{user} add your product {title} with description {desc} in favorites!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[author],
        fail_silently=False
    )
