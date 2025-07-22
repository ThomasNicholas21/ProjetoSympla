from django.db import models
from events.models import Batch


class Log(models.Model):
    batch = models.ForeignKey(
        Batch,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    message = models.TextField()
    imported_amount = models.PositiveIntegerField()
    status = models.CharField(
        max_length=128,
        choices=(
            ('sucess', 'Sucess'),
            ('error', 'Error'),
        )
    )
    created_at = models.DateTimeField(auto_now_add=True)
