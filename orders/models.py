from django.db import models
from products.models import Product
from accounts.models import Profile


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    pick_up = models.CharField(max_length=200)
    payment = models.CharField(max_length=50, blank=True, null=True)
    status = models.BooleanField(default=False)
    total_price = models.IntegerField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.first_name


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user}"


class CartProduct(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.product} - {self.profile}"


class Coupon(models.Model):
    code = models.CharField(max_length=75, unique=True)
    price = models.FloatField(help_text="Enter in USA dollars($)")


class City(models.Model):
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.city


class PickUp(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"
