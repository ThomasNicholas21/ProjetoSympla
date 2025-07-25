from events.tests.test_base import EventsFixture


class TestCategoryModel(EventsFixture):
    def setUp(self):
        self.batch = self.make_batch()
        return super().setUp()

    def test_batch_str_method(self):
        self.batch.full_clean()
        self.batch.save()

        self.assertEqual(
            str(self.batch),
            f'Versão: {self.batch.pk}'
        )
