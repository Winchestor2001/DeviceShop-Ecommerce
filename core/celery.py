import os

from celery import Celery
from datetime import timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

day = 1

app.conf.beat_schedule = {
    f'check-meet-every-{day}-day': {
        'task': 'products.tasks.filter_product_sales_task',
        'schedule': timedelta(days=day),
    }
}