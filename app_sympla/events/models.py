from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128)


class Batch(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class Events(models.Model):
    name = models.CharField(max_length=128)
    start_date = models.DateTimeField()
    location = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    sympla_id = models.CharField(max_length=128, unique=True)
    batch = models.ForeignKey(
        Batch,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
