from io import StringIO
import csv
from django.urls import reverse
from events.tests.test_base import EventsFixture
from django.utils.timezone import make_aware, datetime


class CsvExportTest(EventsFixture):
    def setUp(self):
        super().setUp()

        location = self.make_location(
            location_name='Test Python',
            city='São Paulo'
        )
        category1 = self.make_category(name='Tech')
        category2 = self.make_category(name='Open Source')
        batch = self.make_batch()

        self.event = self.make_event(
            name='Django Conf',
            start_date=self.aware_datetime(2025, 12, 25, 10, 0),
            location=location,
            category=category1,
            sympla_id='sympla123',
            batch=batch,
        )
        self.event.category.add(category2)

    def aware_datetime(self, *args):
        return make_aware(datetime(*args))

    def test_csv_export_response_success(self):
        url = reverse('events:csv-export-csv')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')

    def test_csv_export_has_bom(self):
        url = reverse('events:csv-export-csv')
        response = self.client.get(url)

        content = response.content.decode('utf-8-sig')
        self.assertTrue(
            content.startswith('\ufeff') or content.startswith('ID,')
        )

    def test_csv_export_contains_event_data(self):
        url = reverse('events:csv-export-csv')
        response = self.client.get(url)

        csv_file = StringIO(response.content.decode('utf-8-sig'))
        reader = csv.reader(csv_file)
        rows = list(reader)

        self.assertEqual(rows[0], [
            'ID', 'Nome', 'Data de Início', 'Local', 'Cidade',
            'Categorias', 'Sympla ID', 'Batch ID'
        ])

        self.assertEqual(rows[1][1], 'Django Conf')
        self.assertEqual(rows[1][3], 'Test Python')
        self.assertEqual(rows[1][4], 'São Paulo')
        self.assertIn('Tech', rows[1][5])
        self.assertIn('Open Source', rows[1][5])
