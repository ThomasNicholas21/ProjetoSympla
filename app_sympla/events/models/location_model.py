from django.db import models


class Location(models.Model):
    location_name = models.CharField(max_length=128)
    city = models.CharField(max_length=64)

    def __str__(self):
        return self.location_name
