from django.test import TestCase
from unittest.mock import patch
from requests.exceptions import Timeout, HTTPError
from events.services import sympla_service
import requests


class TestService(TestCase):
    def test_service_exception_timeout(self):
        with patch("requests.get", side_effect=Timeout):
            with self.assertRaises(TimeoutError) as ctx:
                sympla_service("http://fakeurl.com", "fake_token", 100, 1)
            self.assertIn("a requisição expirou.", str(ctx.exception).lower())

    def test_http_error_raises_connection_error(self):
        response = requests.Response()
        response.status_code = 500
        response.reason = "Internal Server Error"
        http_error = HTTPError(response=response)

        with patch("requests.get", side_effect=http_error):
            with self.assertRaises(ConnectionError) as ctx:
                sympla_service("http://fakeurl.com", "fake_token", 100, 1)
            self.assertIn("erro http:", str(ctx.exception).lower())
