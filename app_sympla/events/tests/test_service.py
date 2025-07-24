from django.test import TestCase
from django.utils.timezone import datetime
from unittest.mock import patch, Mock
from requests.exceptions import Timeout, HTTPError, RequestException
from events.services import sympla_service, normalize_data
import requests


class TestService(TestCase):
    def test_service_exception_timeout(self):
        with patch("requests.get", side_effect=Timeout):
            with self.assertRaises(TimeoutError) as exc:
                sympla_service("http://fakeurl.com", "fake_token", 100, 1)
            self.assertIn("a requisição expirou.", str(exc.exception).lower())

    def test_service_http_error(self):
        response = requests.Response()
        response.status_code = 500
        response.reason = "Internal Server Error"
        http_error = HTTPError(response=response)

        with patch("requests.get", side_effect=http_error):
            with self.assertRaises(ConnectionError) as exc:
                sympla_service("http://fakeurl.com", "fake_token", 100, 1)
            self.assertIn("erro http:", str(exc.exception).lower())

    def test_service_request_exception(self):
        with patch(
            "requests.get",
            side_effect=RequestException("Falha geral")
        ):
            with self.assertRaises(ConnectionError) as exc:
                sympla_service("http://fakeurl.com", "fake_token", 100, 1)
            self.assertIn(
                "erro de conexão com a api sympla:",
                str(exc.exception).lower()
            )

    def test_service_invalid_value_error(self):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = ValueError("json inválido")

        with patch("requests.get", return_value=mock_response):
            with self.assertRaises(ValueError) as ctx:
                sympla_service("http://fakeurl.com", "fake_token", 100, 1)
            self.assertIn("parse do json", str(ctx.exception).lower())

    def test_service_normalize_data_event(self):
        data = {
            "name": "   evento teste  ",
            "start_date": datetime(2025, 12, 31, 12, 30),
            "address": {
                "address_num": "123",
                "name": " auditório central ",
                "city": " são paulo "
            },
            "category_prim": {"name": " tecnologia "},
            "category_sec": {"name": " inovação "},
            "id": " ABC123 "
        }

        result = normalize_data(data)

        self.assertEqual(
            result["name"],
            "Evento Teste"
        )
        self.assertEqual(
            result["sympla_id"],
            "abc123"
        )
        self.assertEqual(
            result["start_date"],
            data["start_date"]
        )
        self.assertEqual(
            result["location"]["location_name"],
            "Auditório Central"
        )
        self.assertEqual(
            result["location"]["city"],
            "São Paulo"
        )
        self.assertEqual(
            result["category_prim"],
            "Tecnologia"
        )
        self.assertEqual(
            result["category_sec"],
            "Inovação"
        )

    def test_service_returns_normalized_data(self):
        with patch("events.services.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "data": [
                    {
                        "name": "  evento teste  ",
                        "start_date": datetime(
                            2025, 12, 31, 12, 30
                        ).isoformat(),
                        "address": {
                            "address_num": "123",
                            "name": " auditório central ",
                            "city": " são paulo "
                        },
                        "category_prim": {"name": " tecnologia "},
                        "category_sec": {"name": " inovação "},
                        "id": " ABC123 "
                    }
                ]
            }
            mock_get.return_value = mock_response

            result = sympla_service("https://fakeurl.com", "token", 100, 1)

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['name'], 'Evento Teste')

    def test_service_online_event_location(self):
        data = {
            "name": "Live Online",
            "start_date": datetime(2025, 10, 10, 20, 0),
            "address": {"address_num": "0"},
            "category_prim": {},
            "category_sec": {},
            "id": "event42"
        }

        result = normalize_data(data)

        self.assertEqual(
            result["location"]["location_name"],
            "Evento Online"
        )
        self.assertEqual(
            result["category_prim"],
            ""
        )
        self.assertEqual(
            result["category_sec"],
            ""
        )

    def test_service_missing_address_and_categories(self):
        data = {
            "name": "Sem Local",
            "start_date": datetime(2025, 1, 1, 15, 0),
            "id": "semlocal1"
        }

        result = normalize_data(data)

        self.assertEqual(
            result["location"]["location_name"],
            "Local Não Informado"
        )
        self.assertEqual(
            result["location"]["city"],
            "Cidade Não Informada"
        )
        self.assertEqual(
            result["category_prim"],
            ""
        )
        self.assertEqual(
            result["category_sec"],
            ""
        )

    def test_service_return_has_expected_keys(self):
        data = {
            "name": "Test",
            "start_date": datetime.now(),
            "id": "xpto"
        }

        result = normalize_data(data)
        expected_keys = {
            "name", "start_date", "location",
            "category_prim", "category_sec", "sympla_id"
        }

        self.assertSetEqual(set(result.keys()), expected_keys)
