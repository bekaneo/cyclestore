import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cycle.settings')

app = Celery('cycle')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.update(result_expires=3600, enable_utc=True, timezone='UTC')
app.conf.beat_schedule = {}
app.conf.timezone = 'UTC'
