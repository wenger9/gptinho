from django.contrib import admin

from .models import User, Brand, Region, DataAsset

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_superuser', 'is_staff')


class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mtm_id')


class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mtm_id')


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(DataAsset)
