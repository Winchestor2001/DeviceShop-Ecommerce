from django.db import models
from accounts.models import Profile
from django.utils.text import slugify


class MainCategory(models.Model):
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    photo = models.ImageField(upload_to="banner/", default=None)
    name = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(MainCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    slug = models.SlugField(blank=True, null=True)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    brand = models.CharField(max_length=50)
    supplier = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.TextField()
    state = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.brand} {self.name}"


class Review(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    stars = models.IntegerField()
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def str(self):
        return f"{self.user}"


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='reviews/')

    def str(self):
        return f"{self.review}"


class ProductSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale = models.IntegerField()
    date = models.DateField()

    def str(self):
        return f"{self.product} {self.sale}"


class ProductPhoto(models.Model):
    photo = models.ImageField(upload_to='products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.photo.url


class SavedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.product} - {self.category.name}"
