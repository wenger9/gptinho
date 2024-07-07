from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class DataAsset(models.Model):
    name = models.CharField(max_length=200)
    top_5 = models.TextField(blank=True, null=True)
    sample_statistics = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        app_label = 'data_assets'


class Brand(models.Model):
    mtm_id = models.IntegerField()
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.name


class Region(models.Model):
    mtm_id = models.IntegerField()
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    brands = models.ManyToManyField(Brand, blank=True, related_name="brand_employees")
    regions = models.ManyToManyField(Region, blank=True, related_name='region_employees')
