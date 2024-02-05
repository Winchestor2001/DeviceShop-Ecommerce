# DeviceShop-Ecommerce


CELERY RUN
```bash
celery -A core worker -l INFO -P eventlet
```

CELERY BEAT RUN
```bash
celery -A core beat -l INFO
```