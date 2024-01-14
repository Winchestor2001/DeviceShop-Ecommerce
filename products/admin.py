from django.contrib import admin
from products import models

admin.site.register(models.Product)
admin.site.register(models.ProductSale)
admin.site.register(models.Review)
admin.site.register(models.ProductPhoto)
admin.site.register(models.SavedProduct)
admin.site.register(models.MainCategory)
admin.site.register(models.Category)
admin.site.register(models.ProductCategory)