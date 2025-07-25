from django.db import models


class BatchManager(models.Manager):
    def prefetch_location_and_category_set(self):
        return self.prefetch_related(
            'event_set__location', 'event_set__category'
        )


class Batch(models.Model):
    objects = BatchManager()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Versão: {self.pk}'
