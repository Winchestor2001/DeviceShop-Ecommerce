from django.contrib import admin
from categories import models

admin.site.register(models.MainCategory)
admin.site.register(models.Category)
admin.site.register(models.ProductCategory)
