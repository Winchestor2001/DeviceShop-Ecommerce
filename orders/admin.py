from django.contrib import admin
from orders import models

admin.site.register(models.Order)
admin.site.register(models.OrderProduct)
admin.site.register(models.CartProduct)
admin.site.register(models.Coupon)
