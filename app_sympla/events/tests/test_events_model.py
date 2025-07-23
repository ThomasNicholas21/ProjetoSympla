from django.core.exceptions import ValidationError
from events.tests.test_base import EventsFixture
from parameterized import parameterized


class TestCategoryModel(EventsFixture):
    def setUp(self):
        self.event = self.create_event()
        return super().setUp()

    @parameterized.expand(
            [
                ('name', 128),
                ('sympla_id', 128),
            ]
    )
    def test_events_name_max_length(self, field, max_length):
        setattr(self.event, field, 'Teste' * max_length)
        with self.assertRaises(ValidationError):
            self.event.full_clean()
