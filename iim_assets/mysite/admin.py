from django.contrib import admin
from mysite import models

# Register your models here.
class AssetAdmin(admin.ModelAdmin):
    list_display = ("asset_code", "name", "accessories", "brand", "model", "serial_number", "user", "location", "note")
    search_fields = ("asset_code", "user")
    ordering = ("asset_code",)

admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.AssetUserProfile)
admin.site.register(models.SystemUser)