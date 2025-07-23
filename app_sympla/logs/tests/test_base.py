from django.test import TestCase
from logs import models


class LogFixture(TestCase):
    def setUp(self):
        return super().setUp()

    def make_batch(self):
        return models.Batch.objects.create()

    def create_log(
        self,
        batch=None,
        message='Test',
        imported_amount=10,
        status='sucess',
    ):
        if batch is None:
            batch = self.make_batch()

        return models.Log.objects.create(
            batch=None,
            message=message,
            imported_amount=imported_amount,
            status=status,
        )
