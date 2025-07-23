from django.db import models
from events.models import Category, Batch


class Events(models.Model):
    name = models.CharField(max_length=128)
    start_date = models.DateTimeField()
    location = models.TextField()
    category = models.ManyToManyField(
        Category,
        null=True,
        blank=True
    )
    sympla_id = models.CharField(max_length=128, unique=True)
    batch = models.ForeignKey(
        Batch,
        on_delete=models.DO_NOTHING,
        blank=True,
    )
