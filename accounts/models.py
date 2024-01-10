from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    photo = models.ImageField('profile/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.full_name
