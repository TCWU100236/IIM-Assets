from django.contrib import admin
from mysite import models

# Register your models here.
class AssetAdmin(admin.ModelAdmin):
    list_display = ("asset_code", "name", "accessories", "brand", "model", "serial_number", "user", "location", "note")
    search_fields = ("asset_code", "user")
    ordering = ("asset_code",)

class AssetUserProfileAdmin(admin.ModelAdmin):
    list_display = ("userid", "username")
    search_fields = ("userid", "username")
    ordering = ("userid",)

admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.AssetUserProfile, AssetUserProfileAdmin)
admin.site.register(models.SystemUser)
admin.site.register(models.StockChecker)