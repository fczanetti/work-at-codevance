import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'workatcodev.settings')

app = Celery('workatcodev')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
