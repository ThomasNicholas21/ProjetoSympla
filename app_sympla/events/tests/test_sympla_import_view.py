from django.urls import reverse, resolve
from unittest.mock import patch
from events.tests.test_base import EventsFixture
from events.views import SymplaImportView
from logs.models import Log


class TestSymplaImportView(EventsFixture):
    def setUp(self):
        self.event = self.make_event()
        return super().setUp()

    def test_sympla_import_view_is_correct(self):
        list_view = resolve(reverse('events:home-view'))
        self.assertIs(list_view.func.view_class, SymplaImportView)

    def test_sympla_import_status_code_200(self):
        response = self.client.get(reverse('events:home-view'))
        self.assertEqual(response.status_code, 200)

    def test_sympla_import_correct_template(self):
        response = self.client.get(reverse('events:home-view'))
        self.assertTemplateUsed(response, 'events/page/sympla.html')

    def test_sympla_import_get_or_create_location_creates_new(self):
        location_data = {
            'location_name': 'Local Teste',
            'city': 'Cidade Teste'
        }
        view = SymplaImportView()
        location = view.get_or_create_location(location_data)

        self.assertIsNotNone(location.id)
        self.assertEqual(location.location_name, 'Local Teste')
        self.assertEqual(location.city, 'Cidade Teste')

    def test_sympla_import_get_or_create_categories(self):
        view = SymplaImportView()

        categories = view.get_or_create_categories(
            "Categoria Teste 1", "", None, "Categoria Teste 2"
        )

        self.assertEqual(len(categories), 2)

        names = [c.name for c in categories]
        self.assertIn("Categoria Teste 1", names)
        self.assertIn("Categoria Teste 2", names)
        self.assertNotIn("", names)
        self.assertNotIn(None, names)

    def test_sympla_import_should_create_event_true_when_different(self):
        view = SymplaImportView()
        location = self.make_location(city='City', location_name='Place')
        category = self.make_category(name='Categoria')

        event = self.make_event(location=location, category=category)
        start_date = event.start_date

        should_create = view.should_create_event(
            last_event=event,
            event_data={
                'name': 'Novo Nome',
                'sympla_id': event.sympla_id
            },
            start_date=start_date,
            location=location,
            categories=[category]
        )

        self.assertTrue(should_create)

    def test_sympla_import_create_log_success_message(self):
        view = SymplaImportView()
        batch = self.make_batch()
        context = {'success': 'Importado com sucesso'}
        view.create_log(batch=batch, context=context, created_count=5)

        log = Log.objects.last()
        self.assertEqual(log.message, 'Importado com sucesso')
        self.assertEqual(log.imported_amount, 5)
        self.assertEqual(log.status, 'success')

    def test_post_creates_events_and_batch(self):
        with patch('events.services.sympla_service') as mock_sympla_service:
            mock_sympla_service.return_value = [
                {
                    "name": "Evento Teste",
                    "start_date": "2025-12-31T12:30:00",
                    "location": {
                        "location_name": "Local Teste",
                        "city": "Cidade Teste"
                    },
                    "category_prim": "Tech",
                    "category_sec": "Python",
                    "sympla_id": "event123"
                }
            ]

            response = self.client.post(reverse('events:home-view'), data={})

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "evento(s) importado(s)")
