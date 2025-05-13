from django.contrib import admin
from mysite import models

# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.StorageLocation)
admin.site.register(models.Asset)