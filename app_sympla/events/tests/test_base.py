from django.test import TestCase
from django.utils.timezone import datetime, make_aware
from events import models


class EventsFixture(TestCase):
    def setUp(self):
        return super().setUp()

    def make_category(self, name='Category Test'):
        return models.Category.objects.create(name=name)

    def make_batch(self):
        return models.Batch.objects.create()

    def create_event(
        self,
        name='Test',
        start_date=None,
        location='Name Test + Location Test',
        category=None,
        sympla_id='dasdg',
        batch=None,
    ):
        if start_date is None:
            start_date = make_aware(datetime(2025, 12, 31, 12, 30))

        if category is None:
            category = self.make_category()

        if batch is None:
            batch = self.make_batch()

        return models.Events.objects.create(
            name=name,
            start_date=start_date,
            location=location,
            category=category,
            sympla_id=sympla_id,
            batch=batch,
        )
