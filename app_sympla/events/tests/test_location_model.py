from django.core.exceptions import ValidationError
from events.tests.test_base import EventsFixture
from parameterized import parameterized


class TestLocationModel(EventsFixture):
    def setUp(self):
        self.location = self.make_location()
        return super().setUp()

    @parameterized.expand(
            [
                ('location_name', 128),
                ('city', 64),
            ]
    )
    def test_location_max_length(self, field, max_length):
        setattr(self.location, field, 'Teste' * max_length)
        with self.assertRaises(ValidationError):
            self.location.full_clean()
