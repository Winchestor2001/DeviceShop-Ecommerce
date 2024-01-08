from django.db import models
from orders.models import Order


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    brand = models.CharField(max_length=50)
    supplier = models.ForeignKey(Order, on_delete=models.CASCADE)
    description = models.TextField()
    state = models.CharField(max_length=50)
    create_at = models.DateField()

    def __str__(self):
        return f"{self.brand} {self.name}"


class Review(models.Model):
    user = models.ForeignKey("", on_delete=models.CASCADE)
    stars = models.IntegerField()
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale = models.IntegerField()
    date = models.DateField()
