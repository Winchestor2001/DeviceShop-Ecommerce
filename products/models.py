from django.db import models
from accounts.models import Profile


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    brand = models.CharField(max_length=50)
    supplier = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.TextField()
    state = models.CharField(max_length=50)
    create_at = models.DateField()

    def __str__(self):
        return f"{self.brand} {self.name}"


class Review(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    stars = models.IntegerField()
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def str(self):
        return f"{self.user}"


class ProductSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale = models.IntegerField()
    date = models.DateField()

    def str(self):
        return f"{self.product} {self.sale}"
    
class ProductPhoto(models.Model):
    photo = models.ImageField(upload_to='products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)