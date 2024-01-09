from django.db import models
from products.models import Product


class MainCategory(models.Model):
    photo = models.ImageField(upload_to="banner/", default=None)
    name = models.CharField(max_length=50)
    
class Category(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)

class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)