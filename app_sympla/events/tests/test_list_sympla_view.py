from events.tests.test_base import EventsFixture
from django.urls import reverse, resolve
from events.views import SymplaListView


class TestListSymplaView(EventsFixture):
    def test_list_sympla_view_is_correct(self):
        list_view = resolve(reverse('events:list-view'))
        self.assertIs(list_view.func.view_class, SymplaListView)

    def test_list_sympla_view_status_code_200(self):
        response = self.client.get(reverse('events:list-view'))
        self.assertEqual(response.status_code, 200)

    def test_list_sympla_view_correct_template(self):
        response = self.client.get(reverse('events:list-view'))
        self.assertTemplateUsed(response, 'events/page/list_sympla.html')

    def test_list_sympla_view_template_loads_batches(self):
        self.make_event()

        response = self.client.get(reverse('events:list-view'))
        content = response.content.decode('utf-8')
        response_context_batches = response.context['batches']

        self.assertIn('Test', content)
        self.assertIn('31/12/2025 12:30', content)
        self.assertIn('Test-Location', content)
        self.assertIn('Test-City', content)
        self.assertIn('Category Test', content)
        self.assertEqual(len(response_context_batches), 1)

    def test_list_sympla_view_template_no_events_in_batches_if_empty(self):
        response = self.client.get(reverse('events:list-view'))
        content = response.content.decode('utf-8')

        self.assertIn(
            'Nenhuma carga foi importada ainda.', content
        )
