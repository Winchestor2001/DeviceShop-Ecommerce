from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.celery import app
from datetime import datetime
from .models import ProductSale


@shared_task()
def filter_product_sales_task():
    date = datetime.now()
    year, month, day = date.year, date.month, date.day

    product_sales = ProductSale.objects.filter(date__year=year, date__month=month, date__day=day)
    sales_len = len(product_sales)
    if product_sales.exists():
        product_sales.delete()
        log_text = "SUCCESS"
    else:
        log_text = "UNSUCCESSFUL"

    return f"{log_text} DELETED: {sales_len} promocodes"

