from django.contrib import admin
from products import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'brand', 'state', 'create_at']
    list_display_links = ['name', 'price']
    list_filter = ['price', 'brand']
    # list_editable = ['state']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(models.ProductSale)
admin.site.register(models.Review)
admin.site.register(models.ProductPhoto)
admin.site.register(models.SavedProduct)
admin.site.register(models.MainCategory)
admin.site.register(models.Category)
admin.site.register(models.ProductCategory)
admin.site.register(models.ReviewImage)
