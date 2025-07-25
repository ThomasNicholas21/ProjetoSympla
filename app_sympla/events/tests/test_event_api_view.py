from rest_framework.test import APIRequestFactory
from django.urls import reverse
from django.utils.timezone import make_aware
from events.tests.test_base import EventsFixture
from events.views import EventAPIView
from datetime import datetime


class TestEventAPIView(EventsFixture):
    def setUp(self):
        self.event = self.make_event(
            name='Evento Teste',
            start_date=make_aware(datetime(2025, 12, 31, 12, 30)),
            sympla_id='sympla123',
        )
        self.url = reverse('events:event-api-view')

    def test_event_api_view_list_events_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)

    def test_event_api_view_list_events_returns_paginated_data(self):
        response = self.client.get(f'{self.url}?page=1&page_size=5')
        self.assertIn('results', response.data)
        self.assertLessEqual(len(response.data['results']), 5)

    def test_event_api_view_filter_by_name(self):
        response = self.client.get(f'{self.url}?name=Evento')
        self.assertEqual(len(response.data['results']), 1)

        response = self.client.get(f'{self.url}?name=Inexistente')
        self.assertEqual(len(response.data['results']), 0)

    def test_event_api_view_filter_by_batch(self):
        response = self.client.get(f'{self.url}?batch={self.event.batch.id}')
        self.assertEqual(len(response.data['results']), 1)

    def test_event_api_view_filter_by_start_date(self):
        data_str = self.event.start_date
        response = self.client.get(f'{self.url}?start_date={data_str}')
        self.assertEqual(len(response.data['results']), 1)

    def test_event_api_view_invalid_page_returns_empty_or_error(self):
        response = self.client.get(f'{self.url}?page=999')
        self.assertEqual(response.status_code, 404)

    def test_event_api_view_pagination_respects_page_size_limit(self):
        for i in range(15):
            self.make_event(
                name=f'Evento {i}',
                start_date=make_aware(datetime(2025, 12, 31, 12, 30)),
                sympla_id=f'sympla{i}',
            )

        response = self.client.get(f'{self.url}?page_size=10')
        self.assertEqual(len(response.data['results']), 10)

    def test_event_api_view_returns_paginated_response(self):
        for i in range(6):
            self.make_event(
                name=f"Evento {i}",
                start_date=make_aware(datetime(2025, 12, 31, 12, 30)),
                sympla_id=f"sympla_{i}",
            )

        response = self.client.get(f"{self.url}?page=1&page_size=5")

        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 5)

    def test_event_api_view_returns_non_paginated_data_when_page_is_none(self):
        class NoPaginationView(EventAPIView):
            pagination_class = None

        factory = APIRequestFactory()
        request = factory.get(self.url)

        view = NoPaginationView.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.data)
        self.assertIsInstance(response.data["data"], list)
        self.assertGreaterEqual(len(response.data["data"]), 1)
