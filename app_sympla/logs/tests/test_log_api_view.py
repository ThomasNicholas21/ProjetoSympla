from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory
from logs.tests.test_base import LogFixture
from logs.views import LogAPIView


class TestLogAPIView(LogFixture):
    def setUp(self):
        self.url = reverse('logs:log-api-view')
        self.log_1 = self.create_log(
            message='Log de teste 1',
            imported_amount=3,
            status='success'
        )
        self.log_2 = self.create_log(
            message='Log de teste 2',
            imported_amount=5,
            status='error'
        )

    def test_list_logs_returns_status_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_logs_returns_paginated_data(self):
        response = self.client.get(self.url + '?page=1&page_size=1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)

    def test_list_logs_returns_all_data_when_not_paginated(self):
        response = self.client.get(f'{self.url}?page_size=10')
        self.assertEqual(len(response.data['results']), 2)
        messages = [log['message'] for log in response.data['results']]
        self.assertIn('Log de teste 1', messages)
        self.assertIn('Log de teste 2', messages)

    def test_list_logs_with_invalid_page_returns_error(self):
        response = self.client.get(self.url + '?page=999')
        self.assertEqual(response.status_code, 404)

    def test_log_api_view_returns_paginated_response(self):
        for iterator in range(6):
            self.create_log(
                message='Log de teste 3',
                imported_amount=3,
                status='success'
            )

        response = self.client.get(f"{self.url}?page=1&page_size=5")

        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 5)

    def test_log_api_view_returns_non_paginated_data_when_page_is_none(self):
        class NoPaginationView(LogAPIView):
            pagination_class = None

        factory = APIRequestFactory()
        request = factory.get(self.url)

        view = NoPaginationView.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.data)
        self.assertIsInstance(response.data["data"], list)
        self.assertGreaterEqual(len(response.data["data"]), 1)
