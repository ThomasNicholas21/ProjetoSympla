from django.test import TestCase
from unittest.mock import patch
from requests.exceptions import Timeout
from events.services import sympla_service


class TestService(TestCase):
    def test_service_exception_timeout(self):
        with patch("requests.get", side_effect=Timeout):
            with self.assertRaises(TimeoutError) as ctx:
                sympla_service("http://fakeurl.com", "fake_token", 100, 1)
            self.assertIn("a requisição expirou.", str(ctx.exception).lower())
