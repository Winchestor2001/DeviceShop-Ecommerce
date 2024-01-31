from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    slug = models.SlugField(blank=True, null=True)
    photo = models.ImageField('profile/', blank=True, null=True, default='profile/default.png')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user.username


class ResetPassword(models.Model):
    url = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)