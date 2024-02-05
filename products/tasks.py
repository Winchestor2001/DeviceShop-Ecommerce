from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.celery import app
from datetime import datetime


@shared_task()
def filter_product_sales_task():
    return "WORKED :)"

