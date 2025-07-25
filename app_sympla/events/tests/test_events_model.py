from django.core.exceptions import ValidationError
from events.tests.test_base import EventsFixture
from events.models import Event
from parameterized import parameterized


class TestEventModel(EventsFixture):
    def setUp(self):
        self.event = self.make_event()
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

    def test_event_manager_get_last_event_is_correct(self):
        for iterator in range(3):
            self.make_event(
                name=f'Test-{iterator}',
            )

        event = Event.objects.filter(name='Test-2').first()
        last_event = Event.objects.get_last_event('dasdg')

        self.assertEqual(last_event, event)

    def test_event_str_method(self):
        self.event.name = 'Testing __str__'
        self.event.full_clean()
        self.event.save()

        self.assertEqual(
            str(self.event),
            'Testing __str__'
        )
