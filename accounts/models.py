from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    photo = models.ImageField('profile/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=30)