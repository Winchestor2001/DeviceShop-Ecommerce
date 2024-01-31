from django.db import models
from products.models import Product
from accounts.models import Profile


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    house = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    zip_code = models.IntegerField()
    message = models.TextField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.user}"


class Coupon(models.Model):
    code = models.CharField(max_length=75)
    price = models.FloatField()
