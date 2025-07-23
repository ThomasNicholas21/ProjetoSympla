from django.db import models


class Location(models.Model):
    location_name = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
