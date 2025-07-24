from django.db import models
from events.models.category_model import Category
from events.models.batch_model import Batch
from events.models.location_model import Location


class Event(models.Model):
    name = models.CharField(max_length=128)
    start_date = models.DateTimeField()
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    category = models.ManyToManyField(
        Category,
        blank=True
    )
    sympla_id = models.CharField(max_length=128)
    batch = models.ForeignKey(
        Batch,
        on_delete=models.DO_NOTHING,
        blank=True,
    )
