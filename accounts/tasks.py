from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_activation_mail(email, activation_code):
    activation_link = f'http://54.93.40.127/account/activation/{activation_code}'
    send_mail(
        'Account activation',
        message=activation_link,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False
    )


@shared_task
def send_restore_password_mail(email, activation_code):
    send_mail(
        subject='Restore password code code',
        message=f'Ваш код {activation_code}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False
    )
