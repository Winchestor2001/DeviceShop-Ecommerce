from django.contrib import admin
from accounts import models

admin.site.register(models.Profile)
admin.site.register(models.ResetPassword)
